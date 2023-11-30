import openai

import gradio as gr

import os

from datetime import datetime

from collections import defaultdict

# Use environment variable for API key

openai.api_key = os.getenv(“OPENAI_API_KEY”)

# Basic rate limiter

class RateLimiter:

    def __init__(self, max_requests, time_window):

        self.max_requests = max_requests

        self.time_window = time_window

        self.timestamps = defaultdict(list)

    def is_allowed(self, session_id):

        now = datetime.now()

        if session_id not in self.timestamps:

            self.timestamps[session_id].append(now)

            return True

        timestamps = self.timestamps[session_id]

        # Remove old timestamps

        self.timestamps[session_id] = [t for t in timestamps if (now – t).seconds <= self.time_window]

        if len(self.timestamps[session_id]) < self.max_requests:

            self.timestamps[session_id].append(now)

            return True

        return False

rate_limiter = RateLimiter(max_requests=5, time_window=60)  # Allow 5 requests per minute

# Store separate conversations for different user sessions

chat_sessions = {}

def chatbot(input, session_id):

    if not input:
        return “Please enter a message.”

    if not rate_limiter.is_allowed(session_id):
        return “Rate limit exceeded. Please wait for a while.”

    # Initialize session if not present

    if session_id not in chat_sessions:

        chat_sessions[session_id] = [

            {“role”: “system”, “content”: “You are a helpful and kind AI Assistant.”}

        ]

    session_messages = chat_sessions[session_id]

    session_messages.append({“role”: “user”, “content”: input})

    try:

        chat = openai.ChatCompletion.create(

            model=”gpt-3.5-turbo”, messages=session_messages

        )

        reply = chat.choices[0].message.content

        session_messages.append({“role”: “assistant”, “content”: reply})

    except Exception as e:

        reply = f”Error: {e}”

        print(f”Error for session {session_id}: {e}”)  # Basic logging

    return reply

inputs = gr.inputs.Textbox(lines=7, label=”Chat with AI”)

outputs = gr.outputs.Textbox(label=”Reply”)

gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title=”AI Chatbot”,

             description=”Ask anything you want”,

             theme=”compact”, live=False, session=True).launch(share=True)