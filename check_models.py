from groq import Groq
import config

def list_models():
    if not config.GROQ_API_KEY:
        print("Error: GROQ_API_KEY is not set.")
        return

    client = Groq(api_key=config.GROQ_API_KEY)
    
    try:
        print("Fetching available Groq models...")
        models = client.models.list()
        # The Groq API returns a list of models slightly differently, usually in data
        for m in models.data:
            print(f"Model: {m.id}")
            print(f"  Owner: {m.owned_by}")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
