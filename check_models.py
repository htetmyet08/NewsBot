from google import genai
import config

def list_models():
    if not config.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is not set.")
        return

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    
    try:
        print("Fetching available models...")
        # The new SDK might use a different way to list models, checking commonly used method
        # If client.models.list() exists:
        files = client.models.list()
        for m in files:
            print(f"Model: {m.name}")
            print(f"  DisplayName: {m.display_name}")
            print(f"  Supported: {m.supported_generation_methods}")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
