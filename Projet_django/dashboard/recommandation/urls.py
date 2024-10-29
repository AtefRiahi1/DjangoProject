from django.urls import path
from recommandation.views import delete_feedback, detail_recommandation, recommandation_list, recommandations_personnalisees, submit_feedback, update_feedback

urlpatterns = [
    path('', recommandation_list, name='recommandation_list'),  
    path('recommandation/<int:recommandation_id>/', detail_recommandation, name='detail_recommandation'),  # Utiliser recommandation_id ici
    path('recommandations/', recommandation_list, name='liste_recommandations'),  # Garder ce chemin si nécessai
    path('recommandation/<int:recommandation_id>/submit_feedback/', submit_feedback, name='submit_feedback'),
    path('personnalisees/', recommandations_personnalisees, name='recommandations_personnalisees'),  # Corrigé
        path('feedback/delete/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
            path('feedback/update/<int:feedback_id>/', update_feedback, name='update_feedback'),


  # Add this line

]
