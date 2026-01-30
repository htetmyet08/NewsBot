import vertexai
from vertexai.generative_models import GenerativeModel
import config
import os

def check_model_access():
    print(f"Checking Vertex AI Model Access...")
    print(f"Project: {config.GCP_PROJECT_ID}")
    print(f"Location: {config.GCP_LOCATION}")

    if not config.GCP_PROJECT_ID:
        print("Error: GCP_PROJECT_ID is not set in .env")
        return

    try:
        vertexai.init(project=config.GCP_PROJECT_ID, location=config.GCP_LOCATION)
        
        # List available models to debug 404 errors
        print("\nListing available Gemini models in this project/location:")
        from vertexai.preview.generative_models import GenerativeModel
        # Note: Listing models programmatically in Vertex AI can be tricky, 
        # so we will try a few known persistent names.
        
        known_models = [
            "gemini-1.5-flash",
            "gemini-1.5-flash-001",
            "gemini-1.5-flash-002",
            "gemini-1.5-pro",
            "gemini-1.0-pro"
        ]
        
        for name in known_models:
            print(f"Checking {name}...", end=" ")
            try:
                m = GenerativeModel(name)
                # Just checking object creation isn't enough, usually need a call, 
                # but let's try to generate 'hi'
                r = m.generate_content("hi")
                print("OK! ✅")
            except Exception as ex:
                print(f"Failed ({ex}) ❌")

        model_name = "gemini-1.5-flash"
        
        if response and response.text:
            print(f"SUCCESS: Model '{model_name}' is accessible and working.")
            print(f"Response snippet: {response.text.strip()}")
        else:
            print("WARNING: Model loaded but no response text received.")

    except Exception as e:
        print(f"FAILED: Could not access Vertex AI model.")
        print(f"Error details: {e}")
        print("\nTroubleshooting:")
        print("1. Check if 'Vertex AI API' is enabled in Google Cloud Console.")
        print("2. Check if your Service Account has 'Vertex AI User' role.")
        print("3. Check if GOOGLE_APPLICATION_CREDENTIALS path is correct.")

if __name__ == "__main__":
    check_model_access()

