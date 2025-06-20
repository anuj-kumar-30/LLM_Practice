import os
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelConfig:
    """Configuration for AI models"""
    name: str
    api_key_env: str
    model_name: str
    base_url: str

class AIModelManager:
    """Manages AI model configurations and interactions"""
    
    # Model configurations stored as class attribute
    MODELS = {
        '1': ModelConfig(
            name="Gemini",
            api_key_env='GOOGLE_API_KEY',
            model_name='gemini-2.0-flash',
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        ),
        '2': ModelConfig(
            name="Sambanova",
            api_key_env='SAMBANOVA_API_KEY',
            model_name="Llama-4-Maverick-17B-128E-Instruct",
            base_url="https://api.sambanova.ai/v1"
        ),
        '3': ModelConfig(
            name="Cerebras",
            api_key_env='CEREBRAS_API_KEY',
            model_name="llama-4-scout-17b-16e-instruct",
            base_url="https://api.cerebras.ai/v1"
        ),
        '4': ModelConfig(
            name="Nebius",
            api_key_env='NEBIUS_API_KEY',
            model_name="meta-llama/Meta-Llama-3.1-70B-Instruct",
            base_url="https://api.studio.nebius.com/v1/"
        ),
        '5': ModelConfig(
            name="Groq",
            api_key_env='GROQ_API_KEY',
            model_name="qwen-qwq-32b",
            base_url="https://api.groq.com/openai/v1"
        )
    }
    
    SYSTEM_PROMPTS = {
        '1': "You are a very snarky assistant.",
        '2': "You are a very polite assistant.",
        '3': None  # Custom prompt will be set
    }

    def __init__(self, config: ModelConfig):
        self.config = config
        self.api_key = self._get_api_key()
        self.client = self._create_client()
        self.context = []

    def _get_api_key(self) -> str:
        """Get API key from environment variables"""
        api_key = os.getenv(self.config.api_key_env)
        if not api_key:
            raise ValueError(f"API key {self.config.api_key_env} not found in environment variables")
        return api_key

    def _create_client(self) -> OpenAI:
        """Create OpenAI client"""
        try:
            return OpenAI(api_key=self.api_key, base_url=self.config.base_url)
        except Exception as e:
            logger.error(f"Failed to create client: {e}")
            raise

    def set_system_prompt(self) -> None:
        """Set system prompt based on user preference"""
        print("\nChoose AI behavior:")
        print("1. Snarky")
        print("2. Polite") 
        print("3. Custom")
        
        while True:
            choice = input("\nSelect (1-3): ").strip()
            if choice in ['1', '2']:
                prompt = self.SYSTEM_PROMPTS[choice]
                break
            elif choice == '3':
                custom_behavior = input("Enter custom behavior (single word): ").strip()
                if custom_behavior:
                    prompt = f"You are a very {custom_behavior} assistant."
                    break
                else:
                    print("Please enter a valid behavior.")
            else:
                print("Please select 1, 2, or 3.")
        
        self.context = [{'role': 'system', 'content': prompt}]
        logger.info(f"System prompt set: {prompt}")

    def get_response(self, message: str) -> Optional[str]:
        """Get response from AI model"""
        self.context.append({'role': 'user', 'content': message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=self.context
            )
            
            ai_response = response.choices[0].message.content
            self.context.append({'role': 'assistant', 'content': ai_response})
            return ai_response
            
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return f"Error: {e}"

    def chat_loop(self) -> None:
        """Main chat interaction loop"""
        print(f"\n=== {self.config.name} Chat Started ===")
        print("Type 'quit' to exit")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                
                if not user_input:
                    print("Please enter a message.")
                    continue
                
                response = self.get_response(user_input)
                print(f"AI: {response}")
                
            except KeyboardInterrupt:
                print("\n\nChat interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"Unexpected error in chat loop: {e}")
                print(f"An error occurred: {e}")

def display_model_menu() -> None:
    """Display available models"""
    print("\n=== Available AI Models ===")
    for key, config in AIModelManager.MODELS.items():
        print(f"{key}. {config.name}")

def get_model_choice() -> str:
    """Get user's model choice with validation"""
    while True:
        choice = input(f"\nSelect model (1-{len(AIModelManager.MODELS)}): ").strip()
        if choice in AIModelManager.MODELS:
            return choice
        else:
            print(f"Please select a number between 1 and {len(AIModelManager.MODELS)}")

def main():
    """Main function to run the chat application"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Display menu and get user choice
        display_model_menu()
        model_choice = get_model_choice()
        
        # Get selected model configuration
        selected_config = AIModelManager.MODELS[model_choice]
        
        # Create model manager and start chat
        model_manager = AIModelManager(selected_config)
        model_manager.set_system_prompt()
        model_manager.chat_loop()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted. Goodbye!")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()