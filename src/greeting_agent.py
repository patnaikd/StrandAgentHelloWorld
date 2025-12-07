import os
import logging
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.anthropic import AnthropicModel

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@tool
def get_greeting(name: str) -> str:
    """
    Generate a personalized greeting for the user.

    Args:
        name (str): The name of the user to greet

    Returns:
        str: A friendly personalized greeting message
    """
    logger.info(f"get_greeting tool called with name: {name}")

    if not isinstance(name, str) or not name.strip():
        logger.warning("Invalid or empty name provided")
        return "Hello there! What's your name?"

    greeting = f"Hello, {name.strip()}! Welcome to Strand Agents. It's great to meet you!"
    logger.info(f"Generated greeting: {greeting}")
    return greeting


# Configure the Anthropic model
model = AnthropicModel(
    client_args={
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
    },
    max_tokens=1024,
    model_id="claude-haiku-4-5-20251001",
    params={
        "temperature": 0.7,
    }
)

# Create the greeting agent with the custom greeting tool
agent = Agent(model=model, tools=[get_greeting])

# Execute the agent with a greeting request
if __name__ == "__main__":
    message = "Please greet me! My name is Deb."
    response = agent(message)
    print(response)
