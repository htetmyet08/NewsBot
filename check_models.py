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
        
        model_name = "gemini-1.5-flash-001"
        print(f"Attempting to load model: {model_name}")
        
        model = GenerativeModel(model_name)
        
        # Quick generation test to verify access
        response = model.generate_content("Hello")
        
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

