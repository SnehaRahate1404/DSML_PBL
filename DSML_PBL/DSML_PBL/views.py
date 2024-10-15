from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
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
    initial_proficiency = float(request.GET.get('initial_proficiency', 60))  # Default to 30 if not provided
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
    request.session['character']=request.GET.get('character')
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
        character=request.session['character']
        # Generate response
        # Assuming generate_conversational_response is synchronous
        print(character)
        response = await sync_to_async(generate_conversational_response)(character, user_message, chat_history)
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
        'decisiontree':'''Total Days Required -  R²: 0.98
Minutes Per Day -  R²: 1.00 ''',
        'linearRegression':"R²: 0.89",
        "gradientMethod":" Minutes per day -  R²:1.00"
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
    # Check if 'minutes' exists in the session
    if 'minutes' in request.session:
        minutes = request.session['minutes']
        print(f"Stored minutes: {minutes}")

    # Ensure that 'chat' exists in the session
    if 'chat' in request.session:
        chat_history = request.session['chat']

        # Check if the chat history is empty
        if not chat_history:
            return HttpResponse('No chat yet.')

        chat_text = ""
        for message in chat_history:
            print(message['user'])  # Log user messages for debugging
            chat_text += message['user'] + ". "

        # Check grammar accuracy of the concatenated chat text
        score, corrected_text = check_text_accuracy(chat_text)

        # Print score to server log for debugging purposes
        print(f"Grammar Accuracy Score: {score}%")



        # Return the accuracy score as an HTTP response
        return render(request,'progess.html',{"time":minutes,"profficiency":score})
        # return HttpResponse(f"Grammar Accuracy Score: {score:.2f}%")
    else:
        # If no chat history is found in the session, return an error message
        return HttpResponse("No chat history found to evaluate accuracy.")



def clear_session(request):
    print(request.session['chat'])
    request.session.flush()  # This will clear the session data
    return HttpResponse("Session cleared.")

def stopchat(request):
    if request.method =='POST':
        data = json.loads(request.body)
        mint = data.get('minutes')
        sec = data.get('seconds')
        print(mint," : ",sec)
        
        print("chat is stoppeed")
        total_minutes = mint + (sec // 60)  # Convert seconds to minutes and add to total minutes

        # Store total minutes in the session
        request.session['minutes'] = total_minutes
        # print(request.session['chat'])
        # request.session.flush()
        return JsonResponse({"redirect_url": "/score"})  # Change to your actual redirect URL
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)
