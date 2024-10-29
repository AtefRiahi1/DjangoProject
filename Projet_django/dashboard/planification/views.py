from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import IrrigationPlan, IrrigationSchedule  
from .forms import IrrigationPlanForm, IrrigationScheduleForm, LocationForm  
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.losses import MeanSquaredError
import os
from datetime import datetime, timedelta
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)
# List all irrigation schedules
WEATHER_API_KEY = '5465bc7d107d41f9a01162729242510'
GEOCODE_API_KEY = 'ce9cf096220d40458d0e3b2502573bf0'
BASE_WEATHER_URL = 'http://api.weatherapi.com/v1/current.json'
BASE_GEOCODE_URL = 'https://api.opencagedata.com/geocode/v1/json'

@login_required
def irrigation_plan_list(request):
    irrigation_plans = IrrigationPlan.objects.filter(user=request.user)  
    return render(request, 'front/irrigplan/myplans.html', {'irrigation_plans': irrigation_plans})

# Create a new irrigation schedule
@login_required  
def irrigation_plan_create(request):
    today = timezone.now()
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
    return render(request, 'front/irrigplan/createplan.html', {'form': form, 'today': today}) 

# Update an existing irrigation schedule
@login_required
def irrigation_plan_update(request, pk):
    today = timezone.now()
    irrigation_plan = get_object_or_404(IrrigationPlan, pk=pk)
    if request.method == 'POST':
        form = IrrigationPlanForm(request.POST, instance=irrigation_plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Irrigation plan updated successfully!')
            return redirect('irrigation_plan_list')  
    else:
        form = IrrigationPlanForm(instance=irrigation_plan)
    
    return render(request, 'front/irrigplan/editplan.html', {'form': form, 'irrigation_plan': irrigation_plan,'today': today})

# Delete an irrigation schedule
@login_required  
def irrigation_plan_delete(request, pk):
  irrigation_plan = get_object_or_404(IrrigationPlan, pk=pk)  
  if request.method == 'POST':
      irrigation_plan.delete()
      messages.warning(request, 'Irrigation plan deleted!')
      return JsonResponse({'success': True})  
    
  return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

def irrigation_plans_view(request):
    plans = IrrigationPlan.objects.all() 
    data = [{
        'title': plan.zone,
        'start': plan.date_heure.strftime('%Y-%m-%d %H:%M:%S'), 
        'description': f"Quantity: {plan.quantite_eau} liters"
    } for plan in plans]

    return JsonResponse(data, safe=False)

#Schedule ----------------------------------------------------------
@login_required
def irrigation_schedule_list(request):

    irrigation_schedules = IrrigationSchedule.objects.filter(user=request.user)  
    return render(request, 'front/irrigplan/myschedule.html', {'irrigation_schedules': irrigation_schedules})

def add_irrigation_schedule(request):
    today = timezone.now()
    if request.method == 'POST':
        form = IrrigationScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()   

            return redirect('irrigation_schedule_list')  
    else:
        form = IrrigationScheduleForm()
    
    return render(request, 'front/irrigplan/addschedule.html', {'form': form,'today': today})

@login_required
def irrigation_schedule_update(request, pk):
    irrigation_schedule = get_object_or_404(IrrigationSchedule, pk=pk, user=request.user)
    irrigation_plans = IrrigationPlan.objects.filter(user=request.user)

    if request.method == 'POST':
        form = IrrigationScheduleForm(request.POST, instance=irrigation_schedule, schedule_instance=irrigation_schedule)
        if form.is_valid():
            updated_schedule = form.save(commit=False)
            updated_schedule.user = request.user
            updated_schedule.save()

            selected_plan_ids = request.POST.getlist('irrigation_plans')
            irrigation_schedule.plans.all().delete()

            for plan_id in selected_plan_ids:
                try:
                    plan = IrrigationPlan.objects.get(id=plan_id)
                    plan.schedule = updated_schedule
                    plan.save()
                except IrrigationPlan.DoesNotExist:
                    continue

            messages.success(request, 'Irrigation schedule updated successfully!')
            return redirect('irrigation_schedule_list')
        else:
            print("Form is invalid:", form.errors) 

    else:
        form = IrrigationScheduleForm(instance=irrigation_schedule, schedule_instance=irrigation_schedule)
    return render(request, 'front/irrigplan/editschedule.html', {
        'form': form,
        'irrigation_schedule': irrigation_schedule,
        'irrigation_plans': irrigation_plans,
    })


@login_required  
def irrigation_schedule_delete(request, pk):
    irrigation_schedule = get_object_or_404(IrrigationSchedule, pk=pk, user=request.user) 
    if request.method == 'POST':
        irrigation_schedule.delete()
        messages.warning(request, 'Irrigation schedule deleted!')
        return JsonResponse({'success': True})  
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

#Ai -------------------------------------------------------------------------------------
def get_current_weather(location):
    
    response = requests.get(f"{BASE_GEOCODE_URL}?q={location}&key={GEOCODE_API_KEY}")
    data = response.json()
    if response.status_code != 200 or not data['results']:
        print("Location not found.")
        return None

    lat = data['results'][0]['geometry']['lat']
    lon = data['results'][0]['geometry']['lng']
    weather_response = requests.get(f"{BASE_WEATHER_URL}?q={lat},{lon}&key={WEATHER_API_KEY}")
    weather_data = weather_response.json()

    if weather_response.status_code != 200:
        print("Failed to retrieve current weather data.")
        return None

    current_weather = {
        'temperature': weather_data['current']['temp_c'],
        'pressure': weather_data['current']['pressure_mb'],
        'humidity': weather_data['current']['humidity'],
        'wind_speed': weather_data['current']['wind_kph']
    }
    return current_weather
def load_model(custom_objects=None):
    return tf.keras.models.load_model("weatherlstm.h5", custom_objects=custom_objects)

def load_model_if_exists():
    if os.path.exists("weatherlstm.h5"):
        return load_model(custom_objects={"mse": MeanSquaredError()})
    return None


# Retrain model if not available
def retrain_model(synthetic_data, time_steps=60, epochs=10):
    X, y = prepare_training_data(synthetic_data, time_steps)
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])),
        Dense(4)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=epochs, batch_size=32, verbose=1)
    model.save("weatherlstm.h5")
    return model

# Create synthetic data
def create_synthetic_data(today_weather, num_samples=720):
    np.random.seed(0)
    synthetic_data = pd.DataFrame({
        'temperature': np.random.normal(loc=today_weather['temperature'], scale=5, size=num_samples),
        'pressure': np.random.normal(loc=today_weather['pressure'], scale=2, size=num_samples),
        'humidity': np.random.normal(loc=today_weather['humidity'], scale=8, size=num_samples),
        'wind_speed': np.random.normal(loc=today_weather['wind_speed'], scale=3, size=num_samples)
    })
    synthetic_data['humidity'] = synthetic_data['humidity'].clip(lower=0, upper=100)
    synthetic_data['wind_speed'] = synthetic_data['wind_speed'].clip(lower=0)
    return synthetic_data

# Prepare training data
def prepare_training_data(synthetic_data, time_steps=60):
    X, y = [], []
    for i in range(len(synthetic_data) - time_steps):
        X.append(synthetic_data.iloc[i:i + time_steps].values)
        y.append(synthetic_data.iloc[i + time_steps].values)
    return np.array(X), np.array(y)

# Forecast using LSTM model
def forecast_future(normalized_data, model, scaler):
    input_data = normalized_data[-60:]
    input_data = input_data.reshape((1, input_data.shape[0], input_data.shape[1]))

    forecast = []
    for _ in range(5 * 144):  
        pred = model.predict(input_data)
        forecast.append(pred)
        input_data = np.append(input_data[:, 1:, :], pred.reshape(1, 1, -1), axis=1)

    forecast = scaler.inverse_transform(np.array(forecast).reshape(-1, normalized_data.shape[1]))
    return forecast

# Determine best irrigation day from forecast and display results
def find_best_irrigation_day(forecast_df):
    temp_min_threshold = 20
    temp_max_threshold = 28
    humidity_min_threshold = 45
    humidity_max_threshold = 70
    wind_speed_max_threshold = 25

    best_day = None
    print("\n5-Day Weather Forecast and Irrigation Suitability:")

    for day, day_data in forecast_df.resample('D'):
        avg_temp = day_data['temperature'].mean()
        avg_humidity = day_data['humidity'].mean()
        max_wind_speed = day_data['wind_speed'].max()

        meets_conditions = (temp_min_threshold <= avg_temp <= temp_max_threshold and
                            humidity_min_threshold <= avg_humidity <= humidity_max_threshold and
                            max_wind_speed <= wind_speed_max_threshold)
        
        suitability = "Suitable" if meets_conditions else "Not Suitable"
        print(f"{day.date()}: Avg Temp: {avg_temp:.2f}°C, Avg Humidity: {avg_humidity:.2f}%, "
              f"Max Wind Speed: {max_wind_speed:.2f} m/s - {suitability}")

        if meets_conditions and best_day is None:
            best_day = day.date()

    return best_day

@login_required
def location_form(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            messages.success(request, f'Location "{location}" submitted successfully!')
            request.session['location'] = location  

            today_weather = get_current_weather(location)
            
            if today_weather:
                synthetic_data = create_synthetic_data(today_weather)
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(synthetic_data)

                model = load_model_if_exists()
                if model is None:
                    model = retrain_model(synthetic_data)

                forecast_data = forecast_future(scaled_data, model, scaler)
                forecast_dates = pd.date_range(start=datetime.now(), periods=720, freq='10min')
                forecast_df = pd.DataFrame(forecast_data, columns=['temperature', 'pressure', 'humidity', 'wind_speed'], index=forecast_dates)

                request.session['forecast_data'] = forecast_df.to_json()

                best_day = find_best_irrigation_day(forecast_df)
                if best_day:
                    request.session['best_day'] = best_day.isoformat()  
                    messages.info(request, f'Best day to irrigate: {best_day}')
                else:
                    request.session['best_day'] = None  
                    messages.info(request, "No optimal day for irrigation found in the next 5 days.")

            return redirect('results_page')

    else:
        form = LocationForm()
    
    return render(request, 'front/irrigplan/locationform.html', {'form': form})



@login_required
def results_view(request):
    best_day_str = request.session.get('best_day')
    forecast_data = request.session.get('forecast_data')
    location = request.session.get('location') 
    if forecast_data:
        forecast_df = pd.read_json(forecast_data)
        forecast_df.index = pd.to_datetime(forecast_df.index)
        daily_forecast = forecast_df.resample('D').mean()
        next_five_days = daily_forecast.head(5)
        
    else:
        next_five_days = None

    has_forecast_data = next_five_days is not None and not next_five_days.empty
    best_day = datetime.fromisoformat(best_day_str) if best_day_str else None

    return render(request, 'front/irrigplan/results.html', {
        'best_day': best_day,
        'forecast_df': next_five_days,
        'has_forecast_data': has_forecast_data,
        'location': location,  
    })

@login_required
def add_irrigation(request):
    if request.method == 'POST':
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        try:
            date_heure = datetime.strptime(date_str, "%b. %d, %Y")
        except ValueError:
            messages.error(request, 'Invalid date format. Please use "Oct. 26, 2024".')
            return redirect('irrigation_plan_list')

        irrigation_plan = IrrigationPlan(
            user=request.user,
            date_heure=date_heure,
            quantite_eau=60.0,  
            zone=location
        )
        irrigation_plan.save()
        return redirect('irrigation_plan_list')
    return redirect('irrigation_plan_list')