from django.shortcuts import render
from about.models import *
from home.models import funFactSection, aboutSection, testimonialsSection

def aboutPageFront(request):
    seo = aboutPageSEO.objects.first()
    aboutpage = aboutPage.objects.first()
    about = aboutSection.objects.first()
    funfact = funFactSection.objects.all()
    teams = teamSection.objects.all()
    testimonials = testimonialsSection.objects.all()

    context = {
        'seo' : seo,
        'aboutpage' : aboutpage,
        'about' : about,
        'funfact' : funfact,
        'teams' : teams,
        'testimonials' : testimonials,
    }

    return render(request, 'front/main/about.html', context)

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)