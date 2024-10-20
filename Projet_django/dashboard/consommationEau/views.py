from django.shortcuts import render, get_object_or_404
from consommationEau.models import consommationEauPageSEO
from home.models import ConsommationEau,testimonialsSection
from django.contrib.auth.decorators import login_required

@login_required(login_url='logIn')
def consommationEauFrontPage(request):
    seo = consommationEauPageSEO.objects.first()
    consommationEaus = ConsommationEau.objects.filter(user=request.user)
    testimonials = testimonialsSection.objects.all()

    context ={
        'seo' : seo,
        'consommationEaus' : consommationEaus,
        'testimonials' : testimonials,

    }
    return render(request, 'front/main/consommationEau.html', context)

@login_required(login_url='logIn')
def consommationEauDetail(request, id):
    consommationEau = get_object_or_404(ConsommationEau, id=id)
    consommationEaus = ConsommationEau.objects.exclude(user=request.user).filter(type_culture=consommationEau.type_culture,phase_culture=consommationEau.phase_culture)



    context = {
        'consommationEau' : consommationEau,
        'consommationEaus' : consommationEaus,
    }
    return render(request, 'front/main/partial/consommationEau-details.html', context)


def error_404(request, exception):
    return render(request, 'error/404.html', status=404)
