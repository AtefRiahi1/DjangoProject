from django.shortcuts import render, get_object_or_404,redirect
from consommationEau.models import consommationEauPageSEO
from home.models import ConsommationEau,testimonialsSection
from django.contrib.auth.decorators import login_required
from consommationEau.forms import *
from django.contrib import messages
import numpy as np
import pandas as pd
from consommationEau.train import train_model
from django.core.paginator import Paginator

@login_required(login_url='logIn')
def consommationEauFrontPage(request):
    seo = consommationEauPageSEO.objects.first()
    consommationEaus = ConsommationEau.objects.filter(user=request.user)
    testimonials = testimonialsSection.objects.all()
    paginator = Paginator(consommationEaus, 6)  # Show 6 zones per page
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)

    context ={
        'seo' : seo,
        'consommationEaus' : consommationEaus,
        'testimonials' : testimonials,
        'page_obj':page_obj,

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

@login_required
def show_prediction(request):
    user = request.user

    model, model_columns = train_model(user)
    seo = consommationEauPageSEO.objects.first()
    testimonials = testimonialsSection.objects.all()


    user_data = ConsommationEau.objects.filter(user=user).values()
    user_df = pd.DataFrame(user_data)

    if not user_df.empty:
        monthly_predictions = []

        for day in range(1, 31):
            last_data = user_df.iloc[-1]
            input_data = {
                'temperature': last_data['temperature'], 
                'humidite': last_data['humidite'],
                'precipitations': last_data['precipitations'],
                'type_culture': last_data['type_culture'],
                'phase_culture': last_data['phase_culture']
            }

            input_df = pd.DataFrame([input_data])
            input_df = pd.get_dummies(input_df, columns=['type_culture', 'phase_culture'], drop_first=True)

            for col in model_columns:
                if col not in input_df.columns:
                    input_df[col] = 0  

            input_df = input_df.reindex(columns=model_columns, fill_value=0)

            daily_prediction = model.predict(input_df)

            monthly_predictions.append(daily_prediction[0]) 

        total_monthly_consumption = round(sum(monthly_predictions), 3)
        context ={
        'seo' : seo,
        'predicted_consumption' : total_monthly_consumption,
        'testimonials' : testimonials,

    }

        return render(request, 'front/main/consommationeau/prediction_mensuelle.html', context)
    else:
        return render(request, 'predictions/prediction.html', {'predicted_consumption': None})
    
@login_required(login_url='logIn')
def irrigationFrontPage(request):
    # Récupérer toutes les irrigations de l'utilisateur connecté
    irrigations = Irrigation.objects.filter(user=request.user)
    paginator = Paginator(irrigations, 6)  # Afficher 6 irrigations par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'irrigations': irrigations,
        'page_obj': page_obj,
    }
    return render(request, 'front/main/irrigation/irrigation_list.html', context)

@login_required(login_url='logIn')
def irrigationDetail(request, id):
    # Récupérer l'irrigation spécifique
    irrigation = get_object_or_404(Irrigation, id=id, user=request.user)
    consommations = irrigation.get_consommations()
    # Optionnel : récupérer les autres irrigations du même type (exclure celle de l'utilisateur si nécessaire)
    similar_irrigations = Irrigation.objects.exclude(user=request.user).filter(type_irrigation=irrigation.type_irrigation)

    context = {
        'irrigation': irrigation,
        'consommations': consommations,
        'similar_irrigations': similar_irrigations,
    }
    return render(request, 'front/main/partial/irrigation-details.html', context)

@login_required(login_url='logIn')
def irrigationCreate(request):
    if request.method == 'POST':
        form = IrrigationForm(request.POST, request.FILES, user=request.user)  # Passer l'utilisateur ici
        if form.is_valid():
            irrigation = form.save(commit=True)  # Cela enregistrera l'irrigation et associera les consommations
            messages.success(request, 'Irrigation created successfully!')
            return redirect('irrigationFrontPage')
    else:
        form = IrrigationForm(user=request.user)  # Passer l'utilisateur ici aussi
    
    context = {
        'title': 'Create Irrigation',
        'form': form,
    }
    return render(request, 'front/main/irrigation/create.html', context)


@login_required(login_url='logIn')
def irrigationEdit(request, id):
    irrigation = get_object_or_404(Irrigation, id=id, user=request.user)
    if request.method == 'POST':
        form = IrrigationForm(request.POST, request.FILES, instance=irrigation, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Irrigation updated successfully!')
            return redirect('irrigationFrontPage')
    else:
        form = IrrigationForm(instance=irrigation, user=request.user)
    
    context = {
        'title': 'Edit Irrigation',
        'irrigation': irrigation,
        'form': form,
    }
    return render(request, 'front/main/irrigation/edit.html', context)

@login_required(login_url='logIn')
def irrigationDelete(request, id):
    irrigation = get_object_or_404(Irrigation, id=id, user=request.user)
    irrigation.delete()
    messages.warning(request, 'Irrigation deleted!')
    return redirect('irrigationFrontPage')

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)
