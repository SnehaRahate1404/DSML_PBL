from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import os
import joblib
from django.conf import settings

# Construct the full path to the model file
model_path = os.path.join(settings.BASE_DIR, 'DSML_PBL', 'model_days.pkl')

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


def aboutUs(request):
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
    return JsonResponse(ls, safe=False)