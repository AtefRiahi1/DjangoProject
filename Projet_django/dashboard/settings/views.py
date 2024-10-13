from django.shortcuts import render
from .models import headerFooterSetting  # Assurez-vous d'importer votre modèle

def my_view(request):
    # Récupérez les paramètres de la base de données
    header_footer_setting = headerFooterSetting.objects.first()  # Récupère la première entrée (ou la seule)
    
    # Vérifiez si l'utilisateur est connecté
    if request.user.is_authenticated:
        button_text = 'Logout'
        button_url = header_footer_setting.header_button_url if header_footer_setting else '/logout'
    else:
        button_text = 'Login'
        button_url = '/login'  # URL de connexion

    context = {
        'button_text': button_text,
        'button_url': button_url,
        'footer_description': header_footer_setting.footer_col1_description if header_footer_setting else '',
        # Ajoutez d'autres éléments de contexte si nécessaire
    }
    return render(request, 'front/base.html', context)
