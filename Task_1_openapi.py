import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get an API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your OpenAI API key.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Hardcoded exchange rates for demonstration
EXCHANGE_RATES = {
    ("EUR", "CZK"): 25.5,
    ("USD", "CZK"): 23.2,
    ("CZK", "EUR"): 1 / 25.5,
    ("CZK", "USD"): 1 / 23.2,
    ("EUR", "USD"): 1.1,
    ("USD", "EUR"): 0.91
}

# Implemented currency conversion logic
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    key = (from_currency.upper(), to_currency.upper())
    rate = EXCHANGE_RATES.get(key)
    if not rate:
        return f"Currency conversion from {from_currency} to {to_currency} is not supported."
    converted = round(amount * rate, 2)
    return f"{amount} {from_currency.upper()} = {converted} {to_currency.upper()}"

# Define the function tool for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert amount from one currency to another using predefined exchange rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "The amount of money to convert.",
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "The currency code to convert from, e.g. 'EUR'.",
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "The currency code to convert to, e.g. 'USD'.",
                    },
                },
                "required": ["amount", "from_currency", "to_currency"],
            },
        },
    }
]

def main():
    print("Currency Conversion Assistant")
    print("Available currencies: EUR, USD, CZK")
    print("Type 'exit' to quit")
    print()

    # System message for the assistant
    system_message = {"role": "system", "content": "You are a helpful AI assistant that can convert currencies."}

    # Keep a conversation history
    messages = [system_message]

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if the user wants to exit
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break

        # Add a user message to the history
        user_message = {"role": "user", "content": user_input}
        messages.append(user_message)

        try:
            # Step 1: Let model decide if function should be called
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message
            messages.append(assistant_message)

            tool_calls = assistant_message.tool_calls
            if tool_calls:
                print("--- Tool call detected ---")

                # Process all tool calls, not just the first one
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    # Manually run the tool
                    if function_name == "convert_currency":
                        function_result = convert_currency(**arguments)

                        # Add tool response to messages
                        tool_message = {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": function_result,
                        }
                        messages.append(tool_message)

                # Step 2: Send function results back to model to continue conversation
                followup = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages
                )

                followup_message = followup.choices[0].message
                messages.append(followup_message)

                print("Assistant:", followup_message.content)
            else:
                # No tool call, print regular model response
                print("Assistant:", assistant_message.content)

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
