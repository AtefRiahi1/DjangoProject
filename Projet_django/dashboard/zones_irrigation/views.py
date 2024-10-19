from django.shortcuts import render, get_object_or_404, redirect
from .models import ZoneIrrigation
from django.http import HttpResponseRedirect
from .forms import ZoneIrrigationForm
from django.contrib.auth.decorators import login_required

@login_required
def zone_list(request):
    print("zone_list called")
    # Filtrer les zones d'irrigation pour n'afficher que celles de l'utilisateur connecté
    zones = ZoneIrrigation.objects.filter(user=request.user)
    return render(request, 'zones_irrigation/zones_index.html', {'zones': zones})

@login_required
def zone_detail(request, id):
    zone = get_object_or_404(ZoneIrrigation, id=id)
    return render(request, 'zones_irrigation/zone_detail.html', {'zone': zone})

@login_required
def zone_create(request):
    if request.method == 'POST':
        form = ZoneIrrigationForm(request.POST)
        if form.is_valid():
            zone = form.save(commit=False)  # Ne pas sauvegarder encore
            zone.user = request.user  # Assigner l'utilisateur connecté
            zone.save()  # Maintenant, sauvegarder l'objet
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
