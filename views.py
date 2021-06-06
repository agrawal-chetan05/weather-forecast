import requests
from django.shortcuts import render, redirect
from .models import city
from .forms import cityForm

def index(request):
    url ='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a7d427a1c416a3cb251a9a2de729aa14'
    
    err_msg=''
    message=''
    message_class=''

    if request.method == 'POST':
        form=cityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = city.objects.filter(name=new_city).count()
            if existing_city_count==0:
                r = requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err_msg='city does not exit'
            else:
                err_msg='city already exist'
        if err_msg:
            message = err_msg
            message_class='In valid'
        else:
            message='city added succesfully'
            message_class='is success'
    
    form = cityForm()
    x = city.objects.all()
    weather_data=[]
    for y in x:
            r = requests.get(url.format(y)).json()
            print(r)
            city_weather={
                'city': y,
                'temperature':r['main']['temp'],
                'pressure':r['main']['pressure'],
                'humidity':r['main']['humidity'],
                'temp_min':r['main']['temp_min'],
                'temp_max':r['main']['temp_max'],
                'description':r['weather'][0]['description'],
                'icon': r['weather'][0]['icon']
            }
            weather_data.append(city_weather)
    
    context={
        'weather_data': weather_data,
        'form':form,
        'message':message,
        'message_class':message_class
         }
    return render(request,'weather/index.html',context)

def delete_city(request,city_name):
    city.objects.get(name=city_name).delete()
    return redirect('home')