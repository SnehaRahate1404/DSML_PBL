from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
def Home(request):
    data={
        'title' : 'Home page'
    }
    return render(request ,'index.html' , data)
       
def aboutUs(request):
    return HttpResponse("Welcome to dsml_pbl")

def characters(request):
    return render(request,"character.html")
       
def chat_farmer(request):
    return render(request,"chat_farmer.html")


def process_voice_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # Process the message and generate a response (example logic)
        bot_response = "I heard you say: " + user_message

        return JsonResponse({'response': bot_response})
