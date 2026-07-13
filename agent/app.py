import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()# The program cannot connect to the API if the key is only stored in the .env file


client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    system_message = "Your name is Sam. You are brilliant, kind, and easy to talk to. You make even the most difficult or boring topics clear, engaging, and fun. You are patient, supportive, and always explain things in a simple, interesting way"
    history = []

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break#if i delete break the program keeps running and treats exit as a normal message.

        history.append({'role': 'user', 'content': user_input})#The program still works, but the conversation becomes less consistent

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=0.7,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()
#This agent is more limited than ChatGPT. It can’t answer every question. For example, when I asked for today’s date, it couldn’t answer. 
# It also gives longer answers and takes more time to get to the point

#refliction
#1)It is like a group chat where one person cannot see the old messages
# To understand what everyone is talking about, you have to show them the previous messages again.
#3)I thought the API key was not working, but the real error was that the .env file was not in the correct location
