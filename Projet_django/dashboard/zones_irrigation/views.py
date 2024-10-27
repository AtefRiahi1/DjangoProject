from django.shortcuts import render, get_object_or_404, redirect
from .models import ZoneIrrigation
from django.http import HttpResponseRedirect
from .forms import ZoneIrrigationForm
from django.contrib.auth.decorators import login_required
from .services import WaterNeedsPredictor
import os

@login_required
def zone_list(request):
    print("zone_list called")
   
    zones = ZoneIrrigation.objects.filter(user=request.user)
    return render(request, 'zones_irrigation/zones_index.html', {'zones': zones})

@login_required
def zone_detail(request, id):
    zone = get_object_or_404(ZoneIrrigation, id=id)
    return render(request, 'zones_irrigation/zone_detail.html', {'zone': zone})

@login_required
def zone_create(request):
    if request.method == 'POST':
        form = ZoneIrrigationForm(request.POST, request.FILES)  
        if form.is_valid():
            zone = form.save(commit=False)  
            zone.user = request.user  
            zone.save() 
            return redirect('zone_list')
    else:
        form = ZoneIrrigationForm()
    return render(request, 'zones_irrigation/zone_form.html', {'form': form})

@login_required
def zone_update(request, id):
    zone = get_object_or_404(ZoneIrrigation, id=id)
    if request.method == 'POST':
        form = ZoneIrrigationForm(request.POST, instance=zone)
        if form.is_valid():
            form.save()
            return redirect('zone_detail', id=zone.id)
    else:
        form = ZoneIrrigationForm(instance=zone)
    return render(request, 'zones_irrigation/zone_form.html', {'form': form})

@login_required
def zone_delete(request, id):
    zone = get_object_or_404(ZoneIrrigation, id=id)
    if request.method == 'POST':
        zone.delete()
        return redirect('zone_list')
    return render(request, 'zones_irrigation/zone_confirm_delete.html', {'zone': zone})


def water_need_prediction(request):
    # Retrieve all zones associated with the logged-in user
    zones = ZoneIrrigation.objects.filter(user=request.user)

    # Initialize an error message variable
    error_message = None

    if request.method == 'POST':
        # Get the selected zone ID from the POST request
        zone_id = request.POST.get('zone_id')
        zone = get_object_or_404(ZoneIrrigation, id=zone_id, user=request.user)
        image_zone = zone.image_zone

        # Check if the zone has an associated image
        if not image_zone:
            error_message = "Cette zone ne possède pas d'image."  # Error if no image
        else:
            image_path = image_zone.path
            predictor = WaterNeedsPredictor()

            try:
                # Call the method to check if there are fruits or vegetables in the image
                detected_items = predictor.is_fruit_or_vegetable(image_path)

                if not detected_items:  # If no items are detected, set an error message
                    error_message = "Aucun fruit ou légume détecté dans l'image."
                else:
                    # Attempt to predict the water needs based on the image and zone superficie
                    predicted_label, besoin_eau = predictor.predict(image_path, zone.superficie)

                    # Render the template with the prediction results and detected items
                    return render(request, 'zones_irrigation/water_need_prediction.html', {
                        'besoin_eau': besoin_eau,
                        'predicted_label': predicted_label,
                        'zones': zones
                    })
            except ValueError as ve:
                error_message = f"Erreur lors de la prédiction : {ve}"
            except Exception as e:
                error_message = f"Erreur inattendue : {e}"

    # Render the template with any errors encountered or the list of zones
    return render(request, 'zones_irrigation/water_need_prediction.html', {
        'zones': zones,
        'error': error_message,  # Display error message if any
    })