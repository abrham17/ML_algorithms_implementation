import google.generativeai as genai
import os
import json
from django.conf import settings
from .tools import TOOLS_SCHEMA, handle_function_call

# Configure Gemini
# NOTE: User needs to set GOOGLE_API_KEY in environment
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash', tools=[TOOLS_SCHEMA])

class MCPProcessor:
    def process_message(self, user_message, user_context=None):
        """
        Process a user message using Gemini and execute function calls if needed.
        """
        chat = model.start_chat(enable_automatic_function_calling=True)
        
        # Prepare context prompt if needed
        context_prompt = ""
        if user_context:
            context_prompt = f"Context: {user_context}\n"
        
        response = chat.send_message(f"{context_prompt}{user_message}")
        
        # The library handles automatic function calling, but we might want manual control
        # For this implementation, we rely on the library execution or response text.
        
        return response.text
