from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import IrrigationPlan  
from .forms import IrrigationPlanForm  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# List all irrigation schedules
# List all irrigation schedules
@login_required
def irrigation_plan_list(request):
    irrigation_plans = IrrigationPlan.objects.filter(user=request.user)  
    return render(request, 'front/irrigplan/myplans.html', {'irrigation_plans': irrigation_plans})

# Create a new irrigation schedule
@login_required  
def irrigation_plan_create(request):
    if request.method == 'POST':
        form = IrrigationPlanForm(request.POST)  
        if form.is_valid():
            irrigation_plan = form.save(commit=False) 
            irrigation_plan.user = request.user 
            irrigation_plan.save() 
            messages.success(request, 'Irrigation plan created successfully!')
            return redirect('irrigation_plan_list') 
    else:
        form = IrrigationPlanForm()  
    return render(request, 'front/irrigplan/createplan.html', {'form': form}) 

# Update an existing irrigation schedule
@login_required
def irrigation_plan_update(request, pk):
    irrigation_plan = get_object_or_404(IrrigationPlan, pk=pk)
    if request.method == 'POST':
        form = IrrigationPlanForm(request.POST, instance=irrigation_plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Irrigation plan updated successfully!')
            return redirect('irrigation_plan_list')  # Adjust the redirect URL accordingly
    else:
        form = IrrigationPlanForm(instance=irrigation_plan)
    
    return render(request, 'front/irrigplan/editplan.html', {'form': form, 'irrigation_plan': irrigation_plan})

# Delete an irrigation schedule
@login_required  
def irrigation_plan_delete(request, pk):
  irrigation_plan = get_object_or_404(IrrigationPlan, pk=pk)  
  if request.method == 'POST':
      irrigation_plan.delete()
      messages.warning(request, 'Irrigation plan deleted!')
      return JsonResponse({'success': True})  # Return a JSON response for AJAX
    
  # If the request method is not POST, we don't need to render any template.
  return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def irrigation_plans_view(request):
    plans = IrrigationPlan.objects.all()  # Retrieve all irrigation plans
    data = [{
        'title': plan.zone,
        'start': plan.date_heure.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as needed
        'description': f"Quantity: {plan.quantite_eau} liters"
    } for plan in plans]

    return JsonResponse(data, safe=False)