from django.shortcuts import render,redirect
from .forms import Trip_form,Search_form,Signup
from django.conf import settings
# Create your views here.
import requests
api_key = settings.GOOGLE_MAPS_API_KEY

def index(request):
    return render(request,"firstapp/index.html")
def trip_form(request):
    form = Trip_form()
    srh_form = Search_form()
    if request.method == "POST":
        form = Trip_form(request.POST)
        srh_form = Search_form(request.POST)
        if form.is_valid():
            from_add = form.cleaned_data["from_add"]
            to_add = form.cleaned_data["to_add"]
            request.session["from_add"] = from_add
            request.session["to_add"] = to_add
            return redirect("drt")
        if srh_form.is_valid():
            place_add = srh_form.cleaned_data["place"]
            area_add = srh_form.cleaned_data["area"]
            request.session["place"] = place_add
            request.session["area"] = area_add
            return redirect("drt")
    user = str(request.user)
    return render(request,"firstapp/trip_form.html",{"form":form,"srh_form":srh_form,"user":user})
def latlng_to_place(loc1,loc2):
    api_url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={loc1},{loc2}&key={api_key}'
    resp = requests.get(api_url)
    response = resp.json()
    address = ""
    for loc in response["results"]:
        address = loc["formatted_address"].split(",")[0:2] # "San Francisco, CA, USA"
    return address

def place_to_latlng(addrs):
    api_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={addrs}&key={api_key}'
    resp = requests.get(api_url)
    response = resp.json()
    latitude = ""
    longitude = ""
    for dict in response["results"]:
        latitude = dict["geometry"]["location"]["lat"]
        longitude = dict["geometry"]["location"]["lng"]
        break
    return latitude,longitude

origin = ""
destination = ""
def directions(request,frm_add=None,t_add=None):
    origin = request.session["From"]
    destination = request.session["To"]
    if frm_add != None and t_add != None:
        origin = frm_add
        destination = t_add
    api_url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}'
    resp = requests.get(url=api_url)
    response = resp.json()
    distance = ""
    duration = ""
    end_add = ""
    start_add = ""
    legs = []
    dict_lists = []
    for elements in response["routes"]:
        for element_dict in elements["legs"]:
            legs.append(element_dict)
    for dict in legs:
        distance = dict["distance"]
        duration = dict["duration"]
        end_add = dict["end_address"]
        start_add = dict["start_address"]
        steps = dict["steps"]
        step_dict = {}
        for items in steps:
            step_dict["Distance"] = items["distance"]
            step_dict["Duration"] = items["duration"]
            end_location = latlng_to_place(items["end_location"]["lat"],items["end_location"]["lng"])
            start_location = latlng_to_place(items["start_location"]["lat"], items["start_location"]["lng"])
            step_dict["Start_location"] = start_location
            step_dict["End_location"] = end_location
            step_dict["Instruction"] = items["html_instructions"]
        dict_lists.append(step_dict)
    messages = []
    for msg in dict_lists:
        str1 = f'From {msg["Start_location"]}, You Should {msg["Instruction"]} , then you reach {msg["End_location"]}, which covers {msg["Distance"]} in {msg["Duration"]}'
        messages.append(str1)
    return render(request,"firstapp/directions.html",{"distance":distance,"duration":duration,"end_add":end_add ,"start_add":start_add,"messages":messages,"api_key":api_key})

type_area = ""
def area_type(request):
    place_add = request.session["place"]
    type_area = request.session["area"]
    tuple = place_to_latlng(place_add)
    destination_lat = tuple[0]
    destination_lng = tuple[1]
    api_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={destination_lat},{destination_lng}&radius=2000&keyword={type_area}&key={api_key}'
    resp = requests.get(api_url)
    response = resp.json()
    dict_list = []
    for dict in response["results"]:
        loc_dict = {}
        loc_dict["Name"] = dict["name"]
        if dict["opening_hours"]["open_now"] == True:
            loc_dict["Opening_hours"] = "Open"
        else:
            loc_dict["Opening_hours"] = "Close"
        loc_dict["Vicinity"] = dict["vicinity"]
        for pht in dict["photos"]:
            loc_dict["Photo_reference"] = pht["photo_reference"]
            loc_dict["max_width"] = pht["width"]
            loc_dict["max_height"] = pht["height"]
            break
        dict_list.append(loc_dict)
    return render(request,"firstapp/area_type.html",{"dict_list":dict_list,"api_key":api_key,"place_add":place_add})

def signup(request):
    form = Signup()
    if request.method == "POST":
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            return redirect('/i')
    return render(request,'firstapp/signup.html',{'form':form})




