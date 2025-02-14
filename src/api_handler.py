from google import genai
import os
from dotenv import load_dotenv

# Load API key securely from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ API Key is missing! Please check your .env file.")

# Initialize Gemini Client
try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    raise RuntimeError(f"❌ Error initializing Gemini Client: {str(e)}")


def call_gemini_api(prompt):
    """Calls Google's Gemini API with error handling."""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-thinking-exp-01-21",  # gemini-2.0-flash
            contents=prompt,
        )
        if not response or not hasattr(response, "text"):
            return "⚠️ No valid response received from the API."
        return response.text
    except genai.APIError as e:
        return f"❌ API Error: {str(e)}"
    except genai.RateLimitError:
        return "⏳ Too many requests! Try again later."
    except genai.AuthenticationError:
        return "🔑 Invalid API key! Check your .env file."
    except Exception as e:
        return f"⚠️ Unexpected Error: {str(e)}"


# Example call
# prompt = "Explain how AI works"
# result = call_gemini_api(prompt)
# print(result)
