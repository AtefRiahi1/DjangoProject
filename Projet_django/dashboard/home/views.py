from django.shortcuts import render
from home.models import *
from about.models import teamSection

# ===============> Front Home Page View <===============

def homePageFront(request):
    meta = homePageSEO.objects.first()
    sliders = sliderSection.objects.all()
    about = aboutSection.objects.first()
    funfacts = funFactSection.objects.all()
    clients = clientSection.objects.all()
    testimonials = testimonialsSection.objects.all()
    teams = teamSection.objects.all()

    context = {
        'meta' : meta,
        'sliders' : sliders,
        'about' : about,
        'funfacts' : funfacts,
        'clients' : clients,
        'testimonials' : testimonials,
        'teams' : teams,
    }
    return render(request, 'front/main/index.html', context)

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)