# Currency Conversion Assistant

A simple interactive currency conversion assistant powered by OpenAI's GPT-4o model. This script allows you to convert between EUR, USD, and CZK currencies using natural language queries.

## Features

- Interactive command-line interface
- Natural language processing for currency conversion requests
- Supports EUR, USD, and CZK currencies
- Maintains conversation context

## Setup

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone this repository or download the script files.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the same directory as the script:
   ```
   cp .env.example .env
   ```

4. Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key
   ```

## Usage

1. Run the script:
   ```
   python Task_1_openapi.py
   ```

2. Enter your currency conversion queries in natural language. For example:
   - "Convert 100 EUR to CZK"
   - "How much is 50 USD in EUR?"
   - "What's 1000 CZK in dollars?"

3. Type `exit`, `quit`, or `bye` to end the conversation.

## Available Currencies

The script supports the following currencies:
- EUR (Euro)
- USD (US Dollar)
- CZK (Czech Koruna)

## Exchange Rates

The script uses hardcoded exchange rates for demonstration purposes:
- 1 EUR = 25.5 CZK
- 1 USD = 23.2 CZK
- 1 EUR = 1.1 USD