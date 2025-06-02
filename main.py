# Imports 
import os # for getting environment variable
from dotenv import load_dotenv # for loading the local .env file environment variables
from openai import OpenAI # For creating AI model with openai

# Creating a basic class for model creation, with openai
'''
We are creating this class so that we don't have repeat our openai config code everytime we want to use some other model.
'''
class OpenAIConfig:
    def __init__(self, api_key, model, base_url):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.context = [
            {'role':'system', 'content': "You are a very snarky assistant."},
        ]

    def Model(self):
        model = OpenAI(
            api_key = self.api_key,
            base_url = self.base_url
        )
        return model
    
    def Response(self, msg, client):
        # client = self.Model() # getting our model instance

        '''formating our messages/context'''
        # checking if we are passing only the user input or not, based on that we will format our messages context
        
        
        # creating a response
        try: 
            res = client.chat.completions.create(
                model = self.model,
                messages = msg
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f"Error: {e}")
    
    # Asking user what kind of behavior they want ai to respond
    def set_sys_prompt(self):
        user_input = input("1. Snarky\n2. Polite\n3. Other\n\nSelect any number: ")
        if user_input=='1':
            pass
        elif user_input == '2':
            self.context = [
                {'role':'system', 'content': 'You are very polite assistant'}
            ]
        elif user_input == '3':
            user_input = input('Custom Behaviour(only write the single word attitude): ')
            self.context = [
                {'role':'system', 'content': f'You are a very {user_input}'}
            ]
        return self.context

# msg = []   
# Asking user to chose from multiple models
def choose_model():
    load_dotenv()
    user_model = input("1. Gemini\n2. Sambanove\n3. Cerebras\n4. Nebius\n5. Groq\n\nModel(select any number: )")

    # '''GEMINI MODEL'''
    if user_model == '1':
        # gemini_model = self.Model()
        gemini_model = OpenAIConfig(
            os.getenv('GOOGLE_API_KEY'),
            'gemini-2.0-flash',
            "https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        client = gemini_model.Model()
        gemini_model.context = gemini_model.set_sys_prompt()
        print(gemini_model.context)
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break

            gemini_model.context.append({'role':"user", 'content': user_input})
            res = gemini_model.Response(gemini_model.context,client)
            print(f"AI: {res}")
            gemini_model.context.append({'role':'system', 'content': res})

    # '''SAMBANOVA CLOUD'''
    elif user_model == '2':
        sambanova_model = OpenAIConfig(
            os.getenv('SAMBANOVA_API_KEY'),
            "Llama-4-Maverick-17B-128E-Instruct",
            "https://api.sambanova.ai/v1",
        )

        client = sambanova_model.Model()
        sambanova_model.context = sambanova_model.set_sys_prompt()
        print(sambanova_model.context)

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break
            sambanova_model.context.append({'role':'user', 'content':user_input})

            res = sambanova_model.Response(sambanova_model.context, client)
            print(f"AI: {res}")
            sambanova_model.context.append({'role':'system', 'content':res})

    # Cerebras Model
    elif user_model == '3':
        cerebras_model = OpenAIConfig(
            os.getenv('CEREBRAS_API_KEY'),
            "llama-4-scout-17b-16e-instruct",
            "https://api.cerebras.ai/v1",
        )

        client = cerebras_model.Model()
        cerebras_model.context = cerebras_model.set_sys_prompt()
        print(cerebras_model.context)

        while True:
            user_input = input("You: ")
            if user_input == 'quit':
                break
            cerebras_model.context.append({'role':'user', 'content':user_input})

            res = cerebras_model.Response(cerebras_model.context, client)
            print(f"AI: {res}")
            cerebras_model.context.append({'role': 'system', 'content': res})

    elif user_model == '4':
        nebius_model = OpenAIConfig(
            os.getenv('NEBIUS_API_KEY'),
            "meta-llama/Meta-Llama-3.1-70B-Instruct",
            "https://api.studio.nebius.com/v1/",
        )

        client = nebius_model.Model()
        nebius_model.context = nebius_model.set_sys_prompt()
        print(nebius_model.context)

        while True:
            user_input = input("You: ")
            if user_input == 'quit':
                break
            nebius_model.context.append({'role':'user', 'content':user_input})

            res = nebius_model.Response(nebius_model.context, client)
            print(f"AI: {res}")
            nebius_model.context.append({'role': 'system', 'content': res})

    elif user_model == '5':
        groq_model = OpenAIConfig(
            os.getenv('GROQ_API_KEY'),
            "qwen-qwq-32b",
            "https://api.groq.com/openai/v1",
        )      

        client = groq_model.Model()
        groq_model.context = groq_model.set_sys_prompt()
        print(groq_model.context)

        while True:
            user_input = input("You: ")
            if user_input == 'quit':
                break
            groq_model.context.append({'role':'user', 'content':user_input})

            res = groq_model.Response(groq_model.context, client)
            print(f"AI: {res}")
            groq_model.context.append({'role': 'system', 'content': res})


if __name__ == '__main__':
    choose_model()