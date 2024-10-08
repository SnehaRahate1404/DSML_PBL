import google.generativeai as genai
import os

genai.configure(api_key='AIzaSyDkk9QzHYqjP4jrMCAApApykKiVnynmhdc')

model = genai.GenerativeModel('gemini-1.5-flash')
chat=model.start_chat(history=[])


while(1):
    # response = model.generate_content(input("your command: \n"))
    command="you have to talk on only indian contitution.not anything else."
    question=input("enter your question:\n")
    question=command+question
    response=chat.send_message(question,stream=True)
    response.resolve()
    res=response.text
    res=res.replace('*',' ')
    print(res)


        