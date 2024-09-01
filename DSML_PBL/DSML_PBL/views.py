from django.http import HttpResponse
from django.shortcuts import render

def Home(request):
    data={
        'title' : 'Home page'
    }
    return render(request ,'index.html' , data)
       
def aboutUs(request):
    return HttpResponse("Welcome to dsml_pbl")
       