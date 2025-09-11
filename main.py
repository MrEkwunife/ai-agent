import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) <= 1:
        print("Usage: uv run main.py YOUR PROMPT")
        sys.exit(1)
    user_prompt = " ".join(sys.argv[1:])

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    client = genai.Client(api_key=api_key)
    responseObject = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
    print(responseObject.text)
    if "--verbose" in user_prompt:
        print(f"User prompt: {user_prompt.replace('--verbose', '')}")
        print(f"Prompt tokens: {responseObject.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {responseObject.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
