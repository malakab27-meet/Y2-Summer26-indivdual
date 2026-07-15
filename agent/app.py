import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()# if i delete this line The program cannot load  the API  key from the .env file


client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    system_message = "Your name is Sam. You are brilliant, kind, and easy to talk to. You make even the most difficult or boring topics clear, engaging, and fun. You are patient, supportive, and always explain things in a simple, interesting way"
    history = []
    total_tokens=0
    total_input_t=0
    total_output_t=0


    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break#if i delete break the program keeps running and treats exit as a normal message.

        history.append({'role': 'user', 'content': user_input})#The program still works, but the conversation becomes less consistent
        print('History so far:', history)

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=0.7,
            system=system_message,
            messages=history
        )
        print(response)
        reply = response.content[0].text

        total_input_t += response.usage.input_tokens
        total_output_t+= response.usage.output_tokens

        estimated_cost = (total_input_t / 1_000_000 * 0.25) + (total_output_t/ 1_000_000 * 1.25)
        estimated_cost_cents = estimated_cost*100
        print(f"Estimated cost:{estimated_cost_cents:.6f} cents")

        

        print(f"Tokens used — In: {response.usage.input_tokens} | Out: {response.usage.output_tokens} | Total: {response.usage.input_tokens + response.usage.output_tokens}")

        total_tokens += response.usage.input_tokens + response.usage.output_tokens
        print(f'total using tokens:{total_tokens}')

        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})



run_chat()
#This agent is more limited than ChatGPT. It can’t answer every question. For example, when I asked for today’s date, it couldn’t answer. 
# It also gives longer answers and takes more time to get to the point

#reflection
#1)It is like a group chat where one person cannot see the old messages
# To understand what everyone is talking about, you have to show them the previous messages again.
#3)I thought the API key was not working, but the real error was that the .env file was not in the correct location

#lab2 
#usage.input_tokens is the number of tokens sent to the model. It includes the system message, the user’s message, and the conversation history
#usage.output_tokens shows how many tokens Claude used to create its answer

#step2
#Temperature controls how random and creative the AI’s responses are. Lower values make the answers more consistent and predictable,
#while higher values make the answers more varied and creative

#step3
#The API needs the full history because it does not remember previous conversations. Sending the history each time helps it keep the conversation consistent
 
#reflection lab2
#1)Tokens are like paying for electricity The more electricity you use, the higher your bill becomes. In the same way, the more tokens a conversation uses, the more it costs
#2)If I Deleted This Line 
# history.append({'role': 'user', 'content': user_input})-The AI no longer receives the user’s new message, so it cannot answer the current question correctly.
# The input token count also becomes smaller because the new message is not sent
#history.append({'role': 'assistant', 'content': reply})-The AI forgets its previous replies, so future responses lose context and become less consistent.
# The history also grows more slowly because assistant messages are missing
#print('History so far:', history)-Nothing changes in the AI’s behavior. It only removes the history from the terminal, making debugging harder
#Bug Diary
#Bug: The program gave an error when calculating the estimated cost
#First guess: I thought the cost formula was wrong
#Real cause: I used different variable names (total_input_t and total_input_tokens). After making the names match the program worked