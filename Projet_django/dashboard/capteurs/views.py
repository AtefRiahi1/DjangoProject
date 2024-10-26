# capteurs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Capteur
from .forms import CapteurForm

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
