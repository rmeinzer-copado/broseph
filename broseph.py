# Import required libraries
# pin installation to the old version with `pip install openai==0.28`
import openai  # OpenAI's Python package for interacting with their API
from dotenv import load_dotenv  # To load environment variables from .env file
import os  # To access environment variables
import panel as pn  # Import Panel for GUI
from greet import greet

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get model's completion based on the messages and other parameters

# Use helper function to make it easier to use prompts and to look at the generated outputs
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(  # Use OpenAI's chat completions endpoint
        model=model,  # Use OpenAI's gpt-3.5-turbo model
        messages=messages,
        temperature=temperature,  # Degree of randomness in model's output
    )
    return response.choices[0].message["content"]

# Function to handle the interactive conversation logic
def collect_messages(_):
    prompt = inp.value_input  # Get user input
    inp.value = ''  # Reset the input field
    context.append({'role':'user', 'content':f"{prompt}"})  # Add user message to context
    
    # Get model's response
    response = get_completion_from_messages(context)
    context.append({'role':'assistant', 'content':f"{response}"})  # Add assistant's response to context

    # Display conversation
    if len(panels) > 0:  # Only show after user's first response
        panels.append(
            pn.Row('You:', pn.pane.Markdown(prompt, width=600))
        )
    panels.append(
        pn.Row('Broseph:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'}))
    )
 
    return pn.Column(*panels)  # Return the complete conversation view

# Initialize Panel's JavaScript and CSS extensions for interactive widgets
pn.extension()

panels = []  # Collect display elements

# Initial message context
context = [ {'role':'system', 'content':"""
You are Broseph, a friendly chatbot surfer bro.\
You are pleasant, funny, witty and charming. You like to joke around a lot.\
First, greet the user with your name and ask for their name.\
Make sure to say you are an "AI chatty bro".\
Incessantly talk about surfing and how awesome you are in a surfer-bro style.\
"""} ]  # accumulate messages

# Create FE UI elements
inp = pn.widgets.TextInput(value="Hi", placeholder=f'{greet("Bro")} Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

# Bind button click to conversation logic
interactive_conversation = pn.bind(collect_messages, button_conversation)

# Build and serve the chat dashboard
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True),
# ).servable()  # make chat dashboard servable

# # serve chat dashboard via panel
# dashboard

)

# serve via CodeSpaces with `python -m panel serve broseph.py`
template = pn.template.FastListTemplate(
    title='Broseph - Your AI Chatty Bro',
    meta_description='Broseph - Your AI Chatty Bro',
    # logo='logo.svg',
    # favicon='favicon.svg',
    busy_indicator=None,
    theme_toggle=False,
    accent='#A01346'
    )
template.main.append(dashboard)  # `dashboard` is Panel layout
template.servable()

template