import os
from dotenv import load_dotenv
from google import genai
from google.genai.client import Client
from google.genai.types import GenerateContentResponse


def main():
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Api key not found")

    client: Client = genai.Client(api_key=api_key)
    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
    )

    if not response.usage_metadata:
        raise RuntimeError("Failed to generate content response")
    prompt_tokens: int | None = response.usage_metadata.prompt_token_count
    response_tokens: int | None = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
