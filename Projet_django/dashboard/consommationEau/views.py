from django.shortcuts import render, get_object_or_404,redirect
from consommationEau.models import consommationEauPageSEO
from home.models import ConsommationEau,testimonialsSection
from django.contrib.auth.decorators import login_required
from consommationEau.forms import *
from django.contrib import messages

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
    return render(request, 'front/main/consommationeau/consommationEau.html', context)

@login_required(login_url='logIn')
def consommationEauDetail(request, id):
    consommationEau = get_object_or_404(ConsommationEau, id=id)
    consommationEaus = ConsommationEau.objects.exclude(user=request.user).filter(type_culture=consommationEau.type_culture,phase_culture=consommationEau.phase_culture)



    context = {
        'consommationEau' : consommationEau,
        'consommationEaus' : consommationEaus,
    }
    return render(request, 'front/main/partial/consommationEau-details.html', context)

@login_required(login_url='logIn')
def consommationEauCreate(request):
    if request.method == 'POST':
        form = ConsommationEauFormF(request.POST, request.FILES)
        if form.is_valid():
            # Ne pas enregistrer l'objet tout de suite
            consommation_eau = form.save(commit=False)
            # Assigner l'utilisateur connecté
            consommation_eau.user = request.user
            # Enregistrer l'objet avec l'utilisateur
            consommation_eau.save()
            messages.success(request, 'Water consumption created successfully!')
            return redirect('consommationEauFrontPage')
    else:
        form = ConsommationEauFormF()
    
    context = {
        'title' : 'Create Consommation Eau',
        'form' : form,
    }
    return render(request, 'front/main/consommationeau/create.html', context)

@login_required(login_url='logIn')
def consommationEauEdit(request, id):
    consommationEau = get_object_or_404(ConsommationEau, id=id)
    if request.method == 'POST':
        form = ConsommationEauFormF(request.POST, request.FILES, instance=consommationEau)
        if form.is_valid():
            form.save()
            messages.success(request, 'Water consumption updated successfully!')
            return redirect('consommationEauFrontPage')
    else:
        form = ConsommationEauFormF(instance=consommationEau)
    
    context = {
        'title': 'Edit Consommation Eau',
        'consommationEau': consommationEau,
        'form': form,
    }
    return render(request, 'front/main/consommationeau/edit.html', context)

@login_required(login_url='logIn')
def consommationEauDelete(request, id):
    consommationEau = get_object_or_404(ConsommationEau, id=id)
    consommationEau.delete()
    messages.warning(request, 'Water consumption deleted!')
    return redirect('consommationEauFrontPage')


def error_404(request, exception):
    return render(request, 'error/404.html', status=404)
