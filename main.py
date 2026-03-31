import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Api key not found")

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="ManicBot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args: argparse.Namespace = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    client: genai.Client = genai.Client(api_key=api_key)
    response: types.GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Failed to generate content response")
    prompt_tokens: int | None = response.usage_metadata.prompt_token_count
    response_tokens: int | None = response.usage_metadata.candidates_token_count

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    print("Response:")
    if response.function_calls is not None:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if (
                function_call_result.parts is None
                or len(function_call_result.parts) == 0
            ):
                raise Exception("function_call_result.parts is empty")
            if function_call_result.parts[0].function_response is None:
                raise Exception("parts 1 function_response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("parts 1 function_response.response is None")
            function_results.append(
                function_call_result.parts[0].function_response.response
            )
            print(f"Calling function: {function_call.name}({function_call.args})")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
