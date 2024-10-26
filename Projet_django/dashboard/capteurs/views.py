from django.shortcuts import render, redirect, get_object_or_404
from .models import Capteur, Mesure
from .forms import CapteurForm, MesureForm
from django.utils.dateparse import parse_date

# List all sensors (Read)
def sensor_list(request):
    sensors = Capteur.objects.all()
    return render(request, 'capteurs/sensor_list.html', {'sensors': sensors})

# Create a new sensor
def sensor_create(request):
    if request.method == 'POST':
        form = CapteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sensor_list')
    else:
        form = CapteurForm()
    return render(request, 'capteurs/sensor_form.html', {'form': form})

# Update an existing sensor
def sensor_update(request, pk):
    sensor = get_object_or_404(Capteur, pk=pk)
    if request.method == 'POST':
        form = CapteurForm(request.POST, instance=sensor)
        if form.is_valid():
            form.save()
            return redirect('sensor_list')
    else:
        form = CapteurForm(instance=sensor)
    return render(request, 'capteurs/sensor_form.html', {'form': form})

# Delete a sensor
def sensor_delete(request, pk):
    sensor = get_object_or_404(Capteur, pk=pk)
    if request.method == 'POST':
        sensor.delete()
        return redirect('sensor_list')
    return render(request, 'capteurs/sensor_confirm_delete.html', {'sensor': sensor})


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

def mesure_create(request, capteur_id):
    capteur = get_object_or_404(Capteur, id=capteur_id)
    if request.method == 'POST':
        form = MesureForm(request.POST)
        if form.is_valid():
            mesure = form.save(commit=False)
            mesure.capteur = capteur
            mesure.save()
            return redirect('mesure_list', capteur_id=capteur.id)
    else:
        form = MesureForm()
    return render(request, 'mesures/mesure_form.html', {'form': form, 'capteur': capteur})

def mesure_delete(request, mesure_id):
    mesure = get_object_or_404(Mesure, id=mesure_id)
    capteur_id = mesure.capteur.id
    mesure.delete()
    return redirect('mesure_list', capteur_id=capteur_id)
