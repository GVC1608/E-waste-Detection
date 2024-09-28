from django.shortcuts import render
from core.forms import ImageForm
from core.models import  Image
from django.views.generic import DetailView
from django.views.generic.edit import  FormMixin
from inference_sdk import InferenceHTTPClient
# Create your views here.
import requests


def get_form(request):

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            print(form.data)
            image = form.save(commit=False)
            image.save()
            image_object = form.instance
            print(image_object.image.url)
            url = "http://127.0.0.1:8000" + image_object.image.url
            # get_response_from_robokey(url)
            result = get_response(url)
            return render(request, "home.html", {'form':form, "img_obj":image_object, "result": result})
        else:
            print(form.errors)
            return render(request, "home.html", {"error":"there is something wrong with form"})
    else:
        form = ImageForm()
        return render(request, "home.html",{"form":form})


def get_response_from_robokey(url):
    print(url)
    params = {
        "api_key":"Pj6OT7t5WktVP58BhGdp",
        "image":url
    }
    main_url = "https://detect.roboflow.com/balanced-e-waste-dataset/3"
    request = requests.request("POST", url=main_url,params=params, verify=False)
    if request.status_code != 200:
        print("api is not working " + str(request.status_code) )
    else:
        print(request.json)

def get_response(url):
    print(url)
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="Pj6OT7t5WktVP58BhGdp"
    )
    try:
        result = CLIENT.infer(str(url), model_id="balanced-e-waste-dataset/3")
        if len(result["predictions"]) != 0:
            return result["predictions"][0]["class"]
        else:
            return "It is not electronic waste."
    except Exception as e:
        return "exception" + e



