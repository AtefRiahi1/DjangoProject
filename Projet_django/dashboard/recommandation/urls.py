from django.urls import path
from recommandation.views import detail_recommandation, recommandation_list, recommandations_personnalisees, submit_feedback

urlpatterns = [
    path('', recommandation_list, name='recommandation_list'),  
    path('recommandation/<int:recommandation_id>/', detail_recommandation, name='detail_recommandation'),  # Utiliser recommandation_id ici
    path('recommandations/', recommandation_list, name='liste_recommandations'),  # Garder ce chemin si nécessai
    path('recommandation/<int:recommandation_id>/submit_feedback/', submit_feedback, name='submit_feedback'),
    path('personnalisees/', recommandations_personnalisees, name='recommandations_personnalisees'),  # Corrigé
  # Add this line

]
