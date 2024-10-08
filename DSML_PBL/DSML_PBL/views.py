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
    request.session['chat']=[]
    request.session.set_expiry(0)
    return render(request,'practise.html')

async def chat(request):
    user_message = request.GET.get('message', None)
    
    # Check if 'chat' exists in session
    has_chat = await sync_to_async(lambda: 'chat' in request.session)()
    if not has_chat:
        await sync_to_async(request.session.__setitem__)('chat', [])
    
    if user_message:
        # Append user message
        # await sync_to_async(lambda: request.session['chat'].append(f"User: {user_message}"))()
        
        # Fetch chat history
        chat_history = await sync_to_async(lambda: list(request.session['chat']))()
        
        # Generate response
        # Assuming generate_conversational_response is synchronous
        response = await sync_to_async(generate_conversational_response)('farmer', user_message, chat_history)
        print("Response collected")
        
        # Append bot response
        dt={
            "user":user_message,
            "bot":response,
        }
        await sync_to_async(lambda: request.session['chat'].append(dt))()
        
        # Mark session as modified
        await sync_to_async(lambda: setattr(request.session, 'modified', True))()
        
        # Convert text response to speech
        # Assuming text_to_speech is asynchronous; if not, wrap it
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
    # Ensure that the 'chat' key exists in the session
    if 'chat' in request.session:
        # Retrieve the chat messages stored in the session
        # print(request.session['chat'])
        if(request.session['chat']==[]):
            return HttpResponse('no chat yet')
        chat_history = request.session['chat']
        chat_text=""
        for i in chat_history:
            print(i['user'])
        # Combine the chat messages into a single text for grammar checking
            chat_text +=i['user']+". "
            
        
        # Calculate the grammar accuracy using the check_text_accuracy function
        score, corrected_text = check_text_accuracy(chat_text)
        
        # Print score to server log for debugging purposes
        print(f"Grammar Accuracy Score: {score}%")
        
        # Return the accuracy score as an HTTP response
        return HttpResponse(f"Grammar Accuracy Score: {score:.2f}%")
    else:
        # If no chat history is found in the session, return an error message
        return HttpResponse("No chat history found to evaluate accuracy.")



def clear_session(request):
    print(request.session['chat'])
    request.session.flush()  # This will clear the session data
    return HttpResponse("Session cleared.")
