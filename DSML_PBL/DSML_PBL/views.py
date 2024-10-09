from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import os
import joblib
from django.conf import settings
from .gpt_questions import generate_conversational_response
from toolbox.text_to_voice import text_to_speech
from toolbox.language_tool import check_text_accuracy
import json
from asgiref.sync import sync_to_async
# Construct the full path to the model file
model_path = os.path.join(settings.BASE_DIR, 'DSML_PBL', 'model_days.pkl')

userinputs=[]

try:
    model_days = joblib.load(model_path)
    print("model_days connected")
except FileNotFoundError as e:
    print(f"Error: {e}")

def Home(request):
    data={
        'title' : 'Home page'
    }
    return render(request ,'index.html' , data)


def result(request):
    # Get initial proficiency and session duration from query parameters
    initial_proficiency = int(request.GET.get('initial_proficiency', 20))  # Default to 30 if not provided
    session_duration = int(request.GET.get('session_duration', 20))  # Default to 10 if not provided

    # Create an empty list to hold the predictions
    predictions = []

    # Loop to generate predictions for different session durations (10, 20, ..., 100 minutes)
    for session in range(session_duration, session_duration+60, 10):  # From 10 to 60 minutes
        input_data = [[initial_proficiency, session]]
        predicted_days = model_days.predict(input_data)
        predictions.append((session, predicted_days[0]))  # Store (session_duration, predicted_days)

    print("Request collected at about")
    print("You can achieve 90% proficiency in the following days for different session durations:")

    # Prepare the response
    ls = []
    for duration, days in predictions:
        dt = {
            "duration": duration,
            "days": float(f"{days:.2f}")  # Format days to two decimal places
        }
        ls.append(dt)
        print(f"For {duration} minutes of session, you can achieve 90% proficiency in {days:.2f} days.")

    # Return a JSON response instead of a simple HttpResponse
    return render(request,'result.html',{'result':ls})

def chatpage(request):
    userinputs=[]
    return render(request,'practise.html')

async def chat(request):
    user_message = request.GET.get('message', None)
    userinputs.append(user_message)
    
    # Check if the 'chat' key exists in the session
    if not await sync_to_async(lambda: 'chat' in request.session)():
        # Initialize the 'chat' key in the session if it does not exist
        await sync_to_async(request.session.__setitem__)('chat', [])

    # Simulate a chatbot response
    print("Chat system open")

    if user_message:
        # Append user message to the session chat history
        await sync_to_async(request.session['chat'].append)(f"User: {user_message}")
        
        # Fetch chat history from the session
        chat_history = await sync_to_async(lambda: request.session['chat'])()
        
        # Generate a response based on the user message and chat history
        response = generate_conversational_response('farmer', user_message, chat_history)
        print("Response collected")
        
        # Append the bot's response to the chat history in the session
        await sync_to_async(request.session['chat'].append)(f"Bot: {response}")

        # Optional: Convert text response to speech
        await text_to_speech(response, voice='en-IN-PrabhatNeural')
    else:
        response = "Chatbot says: Hello! How can I help you?"

    return JsonResponse({'response': response})


def accuracy(request):
    data={
        'decisiontree':'''Total Days Required - MSE: 157.04711508242963, MAE: 9.495566560020992, R²: 0.98
Minutes Per Day - MSE: 4.21e-05, MAE: 0.0029900000000000187, R²: 1.00 ''',
        'linearRegression':"0.91",
        "gradientMethod":"0.87"
    }
    
    return render(request,'accuracy.html',data)

def characters(request):
    with open('C:/study material/ty/dsml/DSML_PROJECT/DSML_PBL/DSML_PBL/templates/data.json', 'r') as file:
        data = json.load(file)
    print(data)
    return render(request, 'characters.html', {'data': data})


def check_grammer(request):
    
    user_message = request.GET.get('message', None)
    print(user_message)
    accuracy,correct_sentence=check_text_accuracy(user_message)
    print(correct_sentence)
    return JsonResponse({"corrected":correct_sentence})

def accuracy_score(request):
    print(userinputs)
    text=""
    for i in userinputs:
        text+=i+". "
    score ,co=check_text_accuracy(text)
    print(score)
    return HttpResponse(score)
