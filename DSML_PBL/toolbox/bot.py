import google.generativeai as genai
import speech_recognition as sr
import edge_tts
import asyncio
import os
import pygame
import tempfile
import re
import language_tool_python 

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

genai.configure(api_key='AIzaSyDkk9QzHYqjP4jrMCAApApykKiVnynmhdc')
model = genai.GenerativeModel('gemini-1.5-flash')

emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbats
                           u"\U000024C2-\U0001F251" 
                           "]+", flags=re.UNICODE)

# Initialize the LanguageTool instance for English
tool = language_tool_python.LanguageTool('en-US')


def summarize_text(text, num_sentences):
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_sentences = [sentence for sentence in sentences if any(word not in stop_words for word in sentence.split())]
    summary = ' '.join(filtered_sentences[:num_sentences])
    return summary

# Function to check and print grammatical errors in a sentence
def check_sentence(sentence):
    matches = tool.check(sentence)
    for match in matches:
        print(f"Error: {match.ruleId}")
        print(f"Message: {match.message}")
        print(f"Incorrect: {sentence[match.offset:match.offset + match.errorLength]}")
        print(f"Suggestions: {', '.join(match.replacements)}")
        print()
    corrected_sentence = language_tool_python.utils.correct(sentence, matches)
    return corrected_sentence, len(matches) == 0

# Function to calculate the percentage of correct sentences in the text
def check_text_accuracy(text):
    sentences = text.split('.')
    total_sentences = len(sentences)
    correct_sentences = 0
    print("total sentences= ",total_sentences)

    for sentence in sentences:
        if sentence.strip():  # Check if the sentence is not empty
            corrected_sentence, is_correct = check_sentence(sentence)
            if is_correct:
                correct_sentences += 1
            print(f"Original Sentence: {sentence}")
            print(f"Corrected Sentence: {corrected_sentence}")
            print()

    if total_sentences == 0:
        return 0.0  # Avoid division by zero
    print("correct sentences=",correct_sentences)
    accuracy = (correct_sentences / total_sentences) * 100
    return accuracy

async def text_to_speech(text, voice='en-US-AriaNeural'):
    try:
        # Create a Communicate instance with the text and voice
        communicate = edge_tts.Communicate(text, voice)
        
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            file_path = temp_audio.name
            await communicate.save(file_path)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Load and play the audio file
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Wait for the playback to finish
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(1)
        
        # Stop playback
        pygame.mixer.music.stop()
        
        # Ensure the file is not in use before deleting
        pygame.mixer.quit()
        
        # Delete the temporary file
        os.remove(file_path)
        
    except edge_tts.exceptions.NoAudioReceived as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

voice_list=["en-IN-PrabhatNeural","ar-EG-SalmaNeural","en-US-AriaNeural"]


# Initialize recognizer
recognizer = sr.Recognizer()
def speakwithbot(arr):
    # Use the microphone as the source for input.
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for speech...")
        audio = recognizer.listen(source)
        
    try:
        # Recognize speech using Google Web Speech API
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)
        text+="."
        text=text.capitalize()
        print("You said: " + text)
        arr.append(text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# speakwithbot()
async def main():
    arr=[]
    a=1;
    name=input("enter your name\n")
    res=f"Hello {name} ! Nice to meet you. What can i do for you.."
    await text_to_speech(str(res), voice='en-IN-PrabhatNeural')
    while(1):
        
        cont = input("Enter 1 to continue or 0 to stop: ")
        if cont == "0":
            print("Stopping the loop.")
            break
        print("your turn:")
        
        response = model.generate_content(speakwithbot(arr))
        # response = model.generate_content(speakwithbot(arr), max_length=50, min_length=20, num_beams=3, temperature=0.7)
        res=response.text
        res=res.replace('#',' ')
        res=res.replace('*',' ')
        res = emoji_pattern.sub(r' ', res)
        res = summarize_text(res, 2)
        print(res)
        await text_to_speech(str(res), voice='en-IN-PrabhatNeural')
    
    print(arr)
    concatenated_text = " ".join(arr)
    accuracy = check_text_accuracy(concatenated_text)
    print(f"Percentage of correct sentences: {accuracy:.2f}%")

        


asyncio.run(main())  