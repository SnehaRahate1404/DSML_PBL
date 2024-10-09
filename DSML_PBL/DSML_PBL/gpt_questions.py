import os
from crewai import Agent, Task, Crew, Process

os.environ["OPENAI_API_BASE"] = 'https://api.groq.com/openai/v1'
    # Set the OpenAI model name
    # os.environ["OPENAI_MODEL_NAME"] = 'llama3-8b-8192'  # Adjust based on available model
os.environ["OPENAI_MODEL_NAME"] = 'llama3-8b-8192'  # Adjust based on available model
    # Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = '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'

def generate_conversational_response(role, user_message, chat_history):
    """
    This function takes the role, user message, and chat history as input and returns an engaging, interesting response.
    The role enhances the conversation by giving context on how the agent should respond.
    """
    # Combine the chat history into a formatted string
    conversation_context = "\n".join(chat_history)

    # Define a dynamic agent for generating responses based on the role
    conversational_agent = Agent(
        role=role,
        goal=f'''Your goal is to respond to the conversation in a way that is interesting, engaging, and informative. 
                You should maintain the flow of the conversation while ensuring it's relevant to the user's input. Your responses should not exceed 30 words.''',
        backstory=f'''You are a highly experienced conversationalist with an engaging personality, perfect for keeping discussions interesting. 
                     You can provide insightful answers or ask follow-up questions to keep the chat going smoothly.''',
        verbose=True,
        allow_delegation=False,
    )

    # Define a task that processes the user input and chat history to return a response
    conversation_task = Task(
        description=f'''Respond to the user's input: "{user_message}" in an engaging and interactive way, using your role: "{role}".
                         Here's the chat history: "{conversation_context}".''',
        agent=conversational_agent,
        expected_output='A conversational, interesting response to the user input while considering the chat history.'
    )

    # Execute the task through a crew
    crew = Crew(
        agents=[conversational_agent],
        tasks=[conversation_task],
        verbose=True,
        process=Process.sequential
    )

    # Run the process and retrieve the response
    crew_output = crew.kickoff()
    response = crew_output.tasks_output[0].raw

    return response

    
def main():
    # Input loop for a continuous chat-like experience
    print("Welcome to the interactive chatbot. Type 'exit' to quit.")

    # Get user-defined role
    role = input("Enter the role for your chatbot (e.g., 'Knowledgeable Expert', 'Friendly Assistant', 'Curious Learner'): ")

    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Generate and print chatbot response
        response = generate_conversational_response(role, user_input)
        print(f"{role}: {response}")
if __name__=="__main__":
    main()