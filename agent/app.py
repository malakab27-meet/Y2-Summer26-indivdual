import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()# if i delete this line The program cannot load  the API  key from the .env file


client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    goal = input("what is your study goal for today?")
    system_message =  f"""
    You are Study Coach, a study assistant
    the student's goal today is :{goal}

    Your job is to help students understand difficult topics, answer study related questions, and explain concepts in a simple and clear way.

    Rules:
    - Always explain topics using simple language and provide examples when needed.
    - Always encourage the student to think and learn step by step.
    - Never give false or made-up information.
    - Never complete homework, quizzes, or exams for the student.

    Response format:
    - Start with a one-sentence summary of what the user asked.
    - Then provide a clear and well-organized explanation.
    - End with one follow-up question to check the student's understanding.
    """
    history = []
    total_tokens=0
    total_input_t=0
    total_output_t=0


    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break#if i delete break the program keeps running and treats exit as a normal message.

        if user_input.lower()=='/summary':
            summary_request = {
        'role': 'user',
        'content': """
        Review the full conversation and give a structured summary of:
        1. The topics discussed
        2. The main ideas the student learned
        3. What the student did well
        4. What the student should practice more
        5. The recommended next step"""

    }
            
            response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=0.7,
            system=system_message,
            messages=history+ [summary_request]
        )
            summary = response.content[0].text
            print(f"summary:\n{summary}")
            continue

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

#LAB 3
#1)The system prompt is like the backstage director of a play. The audience never sees the director, but the director tells the actor how to behave, what role to follow, and how to respond in each scene
#2)When I deleted system=system_message
# - the agent stopped following the instructions I gave it. It did not act like a Study Coach anymore, and its answers became more general and less organized. It also stopped following the rules and the response format I wrote
# One rule line: Never complete homework, quizzes, or exams for the student
#after deleting the rule the agent started giving complete answers instead of only explaining and guiding the student step by step
#After deleting the line “End with one follow-up question to check the student’s understanding,” the agent still explained the topic, but it stopped asking a question at the end
#The answers became less interactive and felt more like normal explanations instead of a study conversation
# Bug Diary
#The bug was that the /summary command was being treated like a normal message. At first, I thought the problem was with the API response, but the real cause was that the summary code and the continue line were not inside the /summary condition. I fixed it by moving the summary API call, the print statement, and continue inside the if user_input.lower() == '/summary' block