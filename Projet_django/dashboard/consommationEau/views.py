from django.shortcuts import render, get_object_or_404,redirect
from consommationEau.models import consommationEauPageSEO
from home.models import ConsommationEau,testimonialsSection
from django.contrib.auth.decorators import login_required
from consommationEau.forms import *
from django.contrib import messages
import numpy as np
import pandas as pd
from consommationEau.train import train_model

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

@login_required
def show_prediction(request):
    user = request.user

    model, model_columns = train_model(user)

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

        total_monthly_consumption = sum(monthly_predictions)

        return render(request, 'front/main/consommationeau/prediction_mensuelle.html', {'predicted_consumption': total_monthly_consumption})
    else:
        return render(request, 'predictions/prediction.html', {'predicted_consumption': None})

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)
