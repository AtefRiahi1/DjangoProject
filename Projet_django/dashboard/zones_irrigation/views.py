from django.shortcuts import render, get_object_or_404, redirect
from .models import ZoneIrrigation , MaintenanceSchedule
from django.http import HttpResponseRedirect
from .forms import ZoneIrrigationForm ,MaintenanceScheduleForm
from django.contrib.auth.decorators import login_required
from .services import WaterNeedsPredictor
import os
from django.core.paginator import Paginator

@login_required
def zone_list(request):
    print("zone_list called")
    
    # Get the zones specific to the logged-in user
    zones = ZoneIrrigation.objects.filter(user=request.user)
    
    # Set up pagination
    paginator = Paginator(zones, 6)  # Show 6 zones per page
    page_number = request.GET.get('page')  # Get the current page number from the query parameters
    page_obj = paginator.get_page(page_number)  # Get the relevant page object

    # Render the template with the paginated zones
    return render(request, 'zones_irrigation/zones_index.html', {'page_obj': page_obj})

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


@login_required
def maintenance_list(request):
    print("maintenance_list called")
    
    # Récupérer les maintenances spécifiques à l'utilisateur connecté
    maintenances = MaintenanceSchedule.objects.filter(zone_irrigation__user=request.user)
    
    # Configuration de la pagination
    paginator = Paginator(maintenances, 6)  # Afficher 6 maintenances par page
    page_number = request.GET.get('page')  # Obtenir le numéro de page actuel depuis les paramètres de requête
    page_obj = paginator.get_page(page_number)  # Obtenir l'objet de page pertinent

    # Rendre le template avec les maintenances paginées
    return render(request, 'Maintenance_schedule/maintenance_index.html', {'page_obj': page_obj})

@login_required
def maintenance_detail(request, id):
    maintenance = get_object_or_404(MaintenanceSchedule, id=id)
    return render(request, 'Maintenance_schedule/maintenance_detail.html', {'maintenance': maintenance})

@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST)  # Utiliser le formulaire approprié pour MaintenanceSchedule
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.zone_irrigation = form.cleaned_data['zone_irrigation']  # Assurez-vous de lier la zone d'irrigation
            maintenance.save()
            return redirect('maintenance_list')
    else:
        form = MaintenanceScheduleForm()
    return render(request, 'Maintenance_schedule/maintenance_form.html', {'form': form})

@login_required
def maintenance_update(request, id):
    maintenance = get_object_or_404(MaintenanceSchedule, id=id)
    if request.method == 'POST':
        form = MaintenanceScheduleForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('maintenance_detail', id=maintenance.id)
    else:
        form = MaintenanceScheduleForm(instance=maintenance)
    return render(request, 'Maintenance_schedule/maintenance_form.html', {'form': form})

@login_required
def maintenance_delete(request, id):
    maintenance = get_object_or_404(MaintenanceSchedule, id=id)
    if request.method == 'POST':
        maintenance.delete()
        return redirect('maintenance_list')
    return render(request, 'Maintenance_schedule/maintenance_confirm_delete.html', {'maintenance': maintenance})