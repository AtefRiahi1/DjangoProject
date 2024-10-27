from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Capteur, Mesure
from .forms import CapteurForm, MesureForm

from core.decorators import admin_role_required
from django.utils.dateparse import parse_date
import pickle
import numpy as np
from django.contrib.auth.decorators import login_required



# List all sensors (Read)
def sensor_list(request):
    sensors = Capteur.objects.filter(status=True)
    count = len(sensors)
    return render(request, 'capteurs/sensor_list.html', {'sensors': sensors, 'count': count})

# Create a new sensor
@login_required(login_url='logIn')
@admin_role_required
def sensor_create(request):
    if request.method == 'POST':
        form = CapteurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Capteur ajouté avec succés!')
            return redirect('sensor_list')
    else:
        form = CapteurForm()
    return render(request, 'capteurs/sensor_form.html', {'form': form})

# Update an existing sensor

@login_required(login_url='logIn')
@admin_role_required
def sensor_update(request, pk):
    sensor = get_object_or_404(Capteur, pk=pk)
    if request.method == 'POST':
        form = CapteurForm(request.POST, request.FILES, instance=sensor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Capteur modifié avec succés!')
            return redirect('sensor_list')
    else:
        form = CapteurForm(instance=sensor)
    return render(request, 'capteurs/sensor_form.html', {'form': form})

# Delete a sensor
@login_required(login_url='logIn')
@admin_role_required
def sensor_delete(request, pk):
    sensor = get_object_or_404(Capteur, pk=pk)
    if request.method == 'POST':
        sensor.delete()
        
        messages.success(request, 'Capteur supprimé avec succés!')
        return redirect('sensor_list')
    return render(request, 'capteurs/sensor_confirm_delete.html', {'sensor': sensor})


@login_required(login_url='logIn')
def mesure_list(request, capteur_id):
    capteur = get_object_or_404(Capteur, id=capteur_id)
    mesures = capteur.mesures.all()
     # Filter by date if the search query is present
    search_date = request.GET.get('search_date')
    if search_date:
        try:
            parsed_date = parse_date(search_date)
            if parsed_date:
                mesures = mesures.filter(date_mesure__date=parsed_date)
        except ValueError:
            pass  # Invalid date input will show all results


    return render(request, 'mesures/mesure_list.html', {'capteur': capteur, 'mesures': mesures,'search_date': search_date,})


@login_required(login_url='logIn')
def mesure_create(request, capteur_id):
    capteur = get_object_or_404(Capteur, id=capteur_id)
    if request.method == 'POST':
        form = MesureForm(request.POST)
        if form.is_valid():
            mesure = form.save(commit=False)
            mesure.capteur = capteur
            
            messages.success(request, 'Mesure ajouté avec succés!')
            mesure.save()
            return redirect('mesure_list', capteur_id=capteur.id)
    else:
        form = MesureForm()
    return render(request, 'mesures/mesure_form.html', {'form': form, 'capteur': capteur})


@login_required(login_url='logIn')
def mesure_delete(request, mesure_id):
    mesure = get_object_or_404(Mesure, id=mesure_id)
    capteur_id = mesure.capteur.id
    messages.success(request, 'Mesure supprimé avec succés!')
    mesure.delete()
    return redirect('mesure_list', capteur_id=capteur_id)


# Load the trained model once during app startup
with open('capteurs/utils/irrigation_model.pkl', 'rb') as f:
    model = pickle.load(f)


@login_required(login_url='logIn')
def predict_irrigation(request,sensor_id):
    # Get all measurements for the given sensor
    capteur = get_object_or_404(Capteur, id=sensor_id)
    mesures = capteur.mesures.all()

    # Prepare the input data for prediction
    temperatures = [mesure.temperature for mesure in mesures]
    moistures = [mesure.moisture for mesure in mesures]
    input_data = np.array([temperatures, moistures]).T  # Shape (n, 2)

    # Predict irrigation for each measurement
    predictions = model.predict(input_data)

    # Update the should_irrigate field in Mesure table
    for i, mesure in enumerate(mesures):
        mesure.should_irrigate = bool(predictions[i])
        mesure.save()

    return render(request, 'mesures/irrigation_result.html', {'capteur': capteur, 'mesures': mesures})


# # # # # # # # # # # # # # # # # #
    # Admin Sensor Element #
# # # # # # # # # # # # # # # # # #
@login_required(login_url='logIn')
@admin_role_required
def adminSensorList(request):
    capteurs = Capteur.objects.all()
    context = {
        'title' : 'Capteurs',
        'sensors' : capteurs,
    }
    return render(request, 'dashboard/main/capteursAdmin/list.html', context)


@login_required(login_url='logIn')
@admin_role_required
def adminSensorCreate(request):
    if request.method == 'POST':
        form = CapteurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Capteur ajouté avec succés!')
            return redirect('adminCapteurList')
    else:
        form = CapteurForm()
    context = {
        'title' : 'Ajouter un capteur',
        'form' : form,
    }
    return render(request, 'dashboard/main/capteursAdmin/create.html', context)


@login_required(login_url='logIn')
@admin_role_required
def adminSensorEdit(request, id):
    capteur = get_object_or_404(Capteur, id=id)
    if request.method == 'POST':
        form = CapteurForm(request.POST, request.FILES, instance=capteur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Capteur modifié avec succés!')
            return redirect('adminCapteurList')
    else:
        form = CapteurForm(instance=capteur)

    context = {
        'title' : 'Modifier un capteur',
        'form' : form,
        'sensor' : capteur,
    }
    return render(request, 'dashboard/main/capteursAdmin/edit.html', context)



@login_required(login_url='logIn')
@admin_role_required
def adminSensorDelete(request, id):
    capteur = get_object_or_404(Capteur, id=id)
    capteur.delete()
    messages.warning(request, 'Capteur supprimé!')
    return redirect('adminCapteurList')
