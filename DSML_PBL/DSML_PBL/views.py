from django.http import HttpResponse
from django.shortcuts import render
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


# def predict_days_view(request):
#     if request.method == 'POST':
        # initial_proficiency = float(request.POST.get('initial_proficiency'))
        # session_duration = float(request.POST.get('session_duration'))
        
        # # Prepare input data
        # input_data = [[initial_proficiency, session_duration]]
        
        # Make prediction
        # predicted_days = model_days.predict(input_data)[0]
        
        # Pass the result to the template
    #     context = {
    #         'predicted_days': predicted_days,
    #         'initial_proficiency': initial_proficiency,
    #         'session_duration': session_duration,
    #     }
    #     return render(request, 'predict_days_results.html', context)
    
    # return render(request, 'predict_days_form.html')
def aboutUs(request):
    input_data = [[70, 30]]
    predicted_days = model_days.predict(input_data)
    
    print("request collected at about ")
    print("aur ap ",predicted_days, " dino me 90% cross kr sakhate ho .")
    return HttpResponse("Welcome to dsml_pbl")
       