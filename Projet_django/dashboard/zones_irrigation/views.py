from django.shortcuts import render, get_object_or_404, redirect
from .models import ZoneIrrigation
from django.http import HttpResponseRedirect
from .forms import ZoneIrrigationForm
from django.contrib.auth.decorators import login_required
from .services import predict_water_need

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
    # Récupérer les zones d'irrigation associées à l'utilisateur connecté
    zones = ZoneIrrigation.objects.filter(user=request.user)
    
    if request.method == 'POST':  # Changez GET en POST pour permettre le téléchargement de l'image
        zone_id = request.POST.get('zone_id')  # Récupérer l'ID de la zone sélectionnée

        if zone_id:  # Vérifier si une zone a été sélectionnée
            zone = get_object_or_404(ZoneIrrigation, id=zone_id)  # Récupérer l'objet ZoneIrrigation correspondant
            image_zone = zone.image_zone  # Récupérer le chemin de l'image de la zone

            if image_zone:  # Vérifier si le fichier d'image existe
                image_path = image_zone.path  # Utiliser le chemin de l'image enregistrée
                
                # Calcule le besoin en eau
                besoin_eau = predict_water_need(image_path, zone.superficie)
                print(f"Besoin en eau estimé : {besoin_eau} litres")
                # Affiche les résultats dans la page de résultats
                return render(request, 'zones_irrigation/water_need_prediction.html', {'besoin_eau': besoin_eau})
            else:
                return render(request, 'zones_irrigation/water_need_prediction.html', {'zones': zones, 'error': 'Image not provided'})

    # Si la méthode n'est pas POST ou s'il n'y a pas d'ID de zone, afficher le formulaire
    return render(request, 'zones_irrigation/water_need_prediction.html', {'zones': zones})
