# Imports
import os
import json
from openai import OpenAI
import gradio as gr
import sqlite3
import subprocess

# Basic Setup
# These can be used too. Ready for use.
# server = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# gemma = OpenAI(base_url='http://localhost:11434/v1',api_key='ollama')
# openrouter = OpenAI(base_url='https://openrouter.ai/api/v1',api_key=os.getenv('OPENROUTER_API_KEY'))
gemini = OpenAI(base_url='https://generativelanguage.googleapis.com/v1beta/openai/',api_key=os.getenv('GEMINI_API_KEY'))

DB = "D:\ME\llm_engineering\week2\prices.db"
# System Prompt - Speciaclly for the airline use case.
SystemPrompt = [{'role':'system','content':'''You are a helpful assistant for an Airline called FlightAI.
                 Give short, courteous answers, no more than 1 sentence.Always be accurate.
                 If you don't know the answer, say so.'''}]
 
# Setting up tools - Giving hands to our assistant to interact with the database and get/set ticket prices for different cities.
tools = [
    {"type": "function","function": {
        "name": "get_ticket_price",
        "description": "Get the price of a return ticket to the destination city.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The city that the customer wants to travel to",
                    },
                },
            "required": ["destination_city"],
            "additionalProperties": False
            }
        }
    },
    {'type':'function','function': {
        "name": "set_ticket_price",
        "description": "Set the price of a ticket for the destination city.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The destination city ticket price needs to be set."
                },
                "ticket_price_to_set": {
                    "type": "integer",
                    "description": "The Ticket price to set for the destination city.",
                },
            },
            "required": ["destination_city","ticket_price_to_set"],
            "additionalProperties": False
            }
        }
    }
]

# Functions - To get and set ticket prices from / to the database.

# Getting the ticket price.
def get_ticket_price(city):
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT price FROM prices WHERE city = ?', (city.lower(),))
        result = cursor.fetchone()
        return f"Ticket price to {city} is ${result[0]}" if result else "No price data available for this city"

# Setting the ticket price.
def set_ticket_price(city,price):
    print(f"DATABASE TOOL CALLED: Setting price for {city}", flush=True)
    try:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            cursor.execute('insert into prices values (?,?)', (city.lower(),price,)) 
            conn.commit()
            return f"Ticket price for {city} has been set to ${price}"
    except sqlite3.IntegrityError:
        with sqlite3.connect(DB) as conn:
            cursor = conn.cursor()
            print(f"DATABASE TOOL ERROR: Price for {city} already exists", flush=True)
            cursor.execute('update prices set price = ? where city = ? ', (price,city.lower(),))
            print(f"DATABASE TOOL CALLED: Updating price for {city}", flush=True)
            conn.commit()
            return "Price for this city already exists. Prices have been updated instead."
        
# Handling tool calls for the assistant.
def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        # Simple tool call handling based on the function name.
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get('destination_city')
            price_details = get_ticket_price(city)
            responses.append({
                "role": "tool",
                "content": price_details,
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "set_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city= arguments.get('destination_city')
            price = arguments.get('ticket_price_to_set')
            info = set_ticket_price(city,price)
            responses.append({
                "role": "tool",
                "content": info,
                "tool_call_id": tool_call.id
            })
    return responses

# Chat function to interact with the assistant.
def chat(message,history):
    messages = SystemPrompt+[{"role":h["role"], "content":h["content"]} for h in history]+[{'role':'user','content':message}]
    response = gemini.chat.completions.create(model='gemma-4-31b-it', messages=messages, tools=tools)
    while response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        responses = handle_tool_calls(message)
        messages.append(message)
        messages.extend(responses)
        response = gemini.chat.completions.create(model='gemma-4-31b-it', messages=messages, tools=tools)
    return response.choices[0].message.content

# Gradio UI for the assistant.
ui = gr.ChatInterface(
    fn=chat,
    type="messages",
    title="FlightAI Assistant",
    description="Chat with our AI assistant to get ticket prices and more!",
)
ui.launch(inbrowser=True)
