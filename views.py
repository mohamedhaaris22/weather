from django.shortcuts import render,redirect
from .forms import cityform
from .models import city
from django.contrib import messages
import requests
# Create your views here.
def homeview(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=deaff34ace2f7fa1c0acd4cb203e0387&units=metric'
    if request.method=="POST":
        form=cityform(request.POST)
        if form.is_valid():
            ncity=form.cleaned_data['name']
            ccity=city.objects.filter(name=ncity).count()
            if ccity==0:
                res=requests.get(url.format(ncity)).json()
                if res['cod']==200:
                    form.save()
                    messages.success(request,""+ncity+"added successfully")
                else:
                    messages.error(request,""+ncity+"city does not exist")
            else:
                messages.error(request,""+ncity+"city Already exist")
    form=cityform()
    cities=city.objects.all()
    data=[]
    for Cityname in cities:
        res=requests.get(url.format(Cityname)).json()
        city_weather={
            'city':Cityname,
            'temperature':res['main']['temp'],
            'description':res['weather'][0]['description'],
            'country':res['sys']['country'],
            'icon':res['weather'][0]['icon'],
        }
        data.append(city_weather)
        context={'data':data,'form':form}
        

    return render(request,"weather.html",{'data':data,'form':form})

def delete_city(request,Cname):
    city.objects.get(name=Cname).delete()
    messages.success(request,""+Cname+"Removed successfully")
    return redirect("home")