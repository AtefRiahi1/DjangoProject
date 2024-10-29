import logging
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from recommandation.forms import FeedbackForm
from .models import Feedback, Recommandation
logger = logging.getLogger(__name__)

def recommandation_list(request):
    # Récupérer toutes les recommandations existantes dans la base de données
    recommandations = Recommandation.objects.all()

    # Passer les recommandations au template
    context = {
        'recommandations': recommandations,
    }

    return render(request, 'recommandation/listf.html', context)

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Recommandation, Feedback
from .forms import FeedbackForm

@login_required
@login_required
def detail_recommandation(request, recommandation_id):
    recommandation = get_object_or_404(Recommandation, id=recommandation_id)
    feedbacks = Feedback.objects.filter(recommandation=recommandation)  # Récupérer tous les feedbacks

    # Compter le nombre total de feedbacks
    total_feedbacks = feedbacks.count()

    # Récupérer les recommandations basées sur les "likes" de l'utilisateur
    recommandations_personnalisees = get_recommendations_based_on_feedback(request.user)

    if request.method == 'POST':
        return submit_feedback(request, recommandation_id)

    return render(request, 'recommandation/detail_recommandation.html', {
        'recommandation': recommandation,
        'feedbacks': feedbacks,  # Passer les feedbacks au template
        'total_feedbacks': total_feedbacks,
        'recommandations_personnalisees': recommandations_personnalisees,
    })

# views.py
@login_required

def submit_feedback(request, recommandation_id):
    recommandation = get_object_or_404(Recommandation, id=recommandation_id)

    if request.method == 'POST':
        feedback_type = request.POST.get('feedback_type')  # Peut être None
        comment = request.POST.get('comment')  # Commentaire

        # Vérifiez si l'utilisateur a déjà soumis un feedback de ce type
        existing_feedback = Feedback.objects.filter(
            recommandation=recommandation,
            user=request.user,
            feedback_type=feedback_type  # Peut être None
        ).first()

        if existing_feedback:
            messages.error(request, f"Vous avez déjà donné un avis '{feedback_type}' pour cette recommandation.")
        else:
            # Créez un nouveau feedback
            feedback = Feedback(
                recommandation=recommandation,
                user=request.user,
                feedback_type=feedback_type,  # Peut être None ou une valeur valide
                comment=comment or ''  # Le commentaire peut être vide
            )
            feedback.save()
            messages.success(request, "Votre avis a été soumis avec succès.")

        return redirect('detail_recommandation', recommandation_id=recommandation.id)

    return redirect('detail_recommandation', recommandation_id=recommandation.id)


@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.user == feedback.user:
        feedback.delete()
        messages.success(request, "Commentaire supprimé avec succès !")
    else:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce commentaire.")

    # Redirigez l'utilisateur vers la page de détails de la recommandation
    return redirect('detail_recommandation', recommandation_id=feedback.recommandation.id)



@login_required
def update_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)

    # Vérifiez que l'utilisateur est l'auteur du commentaire
    if request.user != feedback.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce commentaire.")
        return redirect('detail_recommandation', recommandation_id=feedback.recommandation.id)

    if request.method == 'POST':
        # Récupérez le nouveau commentaire
        new_comment = request.POST.get('comment')
        feedback.comment = new_comment or ''
        feedback.save()
        messages.success(request, "Votre commentaire a été mis à jour avec succès.")
        return redirect('detail_recommandation', recommandation_id=feedback.recommandation.id)

    # Affichez le formulaire de mise à jour avec l'ancien commentaire
    return render(request, 'recommandation/update_feedback.html', {'feedback': feedback})


def get_recommendations_based_on_feedback(user, limit=2):
    # Récupérer les feedbacks "like" de l'utilisateur
    feedbacks = Feedback.objects.filter(user=user, feedback_type=Feedback.LIKE).select_related('recommandation')

    # Extraire les recommandations likées
    recommandations_likées = [feedback.recommandation for feedback in feedbacks]

    # Si l'utilisateur a déjà liké certaines recommandations
    if recommandations_likées:
        # Extraire les régions et types de culture des recommandations likées
        regions = set(recommandation.region for recommandation in recommandations_likées if recommandation.region)
        crop_types = set(recommandation.crop_type for recommandation in recommandations_likées if recommandation.crop_type)

        # Obtenir des recommandations similaires (par région et type de culture)
        recommandations_similaires = Recommandation.objects.filter(
            region__in=regions,
            crop_type__in=crop_types
        ).exclude(id__in=[rec.id for rec in recommandations_likées])[:limit]

        # Combiner les recommandations likées et similaires, puis limiter à "limit"
        recommendations_personnalisees = list(recommandations_likées) + list(recommandations_similaires)
        return recommendations_personnalisees[:limit]

    # Si l'utilisateur n'a pas encore donné de feedback, retourner des recommandations par défaut (basées sur la région de l'utilisateur par exemple)
    region_utilisateur = user.profile.region if hasattr(user, 'profile') and user.profile.region else 'Sousse'
    return Recommandation.objects.filter(region=region_utilisateur)[:limit]


def recommandations_personnalisees(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        # Récupérer tous les feedbacks de l'utilisateur
        all_feedbacks = Feedback.objects.filter(user=current_user)
        print("Tous les feedbacks de l'utilisateur :", all_feedbacks)

        # Récupérer les feedbacks aimés et dislikés
        liked_feedbacks = Feedback.objects.filter(user=current_user, feedback_type=Feedback.LIKE)
        disliked_feedbacks = Feedback.objects.filter(user=current_user, feedback_type=Feedback.DISLIKE)

        # Debugging : Vérification des feedbacks
        print("Feedbacks aimés récupérés :", liked_feedbacks)
        print("Feedbacks dislikés récupérés :", disliked_feedbacks)

        # Obtenir les types de cultures aimées et dislikées
        liked_crops = liked_feedbacks.values_list('recommandation__crop_type', flat=True).distinct()
        disliked_crops = disliked_feedbacks.values_list('recommandation__crop_type', flat=True).distinct()

        # Affichage des cultures aimées et dislikées
        print("Cultures aimées :", list(liked_crops))
        print("Cultures dislikées :", list(disliked_crops))

        # Initialiser les recommandations basées sur les cultures aimées
        recommandations_personnalisees = Recommandation.objects.filter(crop_type__in=liked_crops)

        # Exclure les recommandations qui correspondent aux types de cultures dislikées
        if disliked_crops.exists():
            recommandations_personnalisees = recommandations_personnalisees.exclude(crop_type__in=disliked_crops)

        # Vérifier si des recommandations sont disponibles
        if recommandations_personnalisees.exists():
            print("Recommandations personnalisées trouvées :", recommandations_personnalisees)
        else:
            print("Aucune recommandation personnalisée trouvée.")

    else:
        recommandations_personnalisees = Recommandation.objects.none()  # Aucune recommandation si non authentifié

    return render(request, 'recommandation/recommandations_personnalisees.html', {
        'recommandations_personnalisees': recommandations_personnalisees
    })
