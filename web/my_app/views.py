import requests
from django.shortcuts import render
from .forms import WeatherForm

def get_weather_data(city):
    api_key = 'b83ab54266114418d641392d8201fd7b'  # add your api key here
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    data = response.json()
    return data

def weather(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather_data = get_weather_data(city)

            if weather_data['cod'] == 200:
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                context = {'temperature': temperature, 'description': description, 'city': city}
            else:
                context = {'error_message': 'City not found'}

            return render(request, 'weather.html', context)
    else:
        form = WeatherForm()

    return render(request, 'weather.html', {'form': form})