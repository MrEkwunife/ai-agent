import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from prompts import system_prompt  # Fixed typo: propmts -> prompts
from call_function import call_function, available_functions

def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}\n")
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    result = generate_content(client, messages, verbose)
    print(result)

def generate_content(client, messages, verbose):
    max_iterations = 20

    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if verbose:
                print(f"Iteration {iteration + 1}:")
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)

            # Add the AI's response (including any function calls) to the conversation
            for candidate in response.candidates:
                messages.append(candidate.content)

            # If there's a text response, we're done
            if response.text:
                if verbose:
                    print("Final response:")
                return response.text

            # Collect function calls from candidates (Gemini nests them in candidate.content.parts)
            function_call_parts = []
            if response.function_calls:
                function_call_parts = response.function_calls
            else:
                # Check candidates for function calls
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call') and part.function_call:
                            function_call_parts.append(part)

            # If no function calls and no text, something's wrong
            if not function_call_parts:
                break

            # Handle function calls
            function_responses = []
            for function_call_part in function_call_parts:
                # Always print function calls (not gated by verbose)
                print(f" - Calling function: {function_call_part.function_call.name}")

                function_call_result = call_function(function_call_part, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")

                function_responses.append(function_call_result.parts[0])

            if not function_responses:
                raise Exception("no function responses generated, exiting.")

            # Add function results to conversation as a user message
            messages.append(types.Content(role="user", parts=function_responses))

        except Exception as e:
            if verbose:
                print(f"Error in iteration {iteration + 1}: {e}")
            return f"Error: {e}"

    return "Error: Maximum iterations reached without a final response."

if __name__ == "__main__":
    main()
