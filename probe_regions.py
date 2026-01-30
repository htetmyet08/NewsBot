import vertexai
from vertexai.generative_models import GenerativeModel
import config
import os

def probe_regions():
    # List of regions to test
    regions = [
        "us-central1",
        "us-west1",
        "us-east4",
        "asia-southeast1", # Singapore
        "europe-west4"     # Netherlands
    ]
    
    project_id = config.GCP_PROJECT_ID
    if not project_id:
        print("Error: GCP_PROJECT_ID not set.")
        return

    print(f"Probing regions for project: {project_id}")
    print("Test Model: gemini-1.5-flash")
    print("-" * 40)

    for loc in regions:
        print(f"Testing location: {loc} ... ", end="")
        try:
            # Re-init vertex ai for each region
            vertexai.init(project=project_id, location=loc)
            model = GenerativeModel("gemini-1.5-flash")
            
            # Try to generate
            response = model.generate_content("hi")
            if response:
                print("SUCCESS! ✅")
                print(f"  >>> FOUND WORKING REGION: {loc}")
                print(f"  >>> Update your .env file: GCP_LOCATION={loc}")
                return
        except Exception as e:
            # Shorten error to keep it readable
            err_str = str(e).split('\n')[0]
            if "404" in err_str:
                print("Not Found (404) ❌")
            elif "403" in err_str:
                print("Forbidden (403) ⛔")
            else:
                print(f"Error: {err_str[:50]}...")

    print("-" * 40)
    print("RESULTS:")
    print("If ALL regions failed with 404/403, you likely need to:")
    print("1. Go to Google Cloud Console > Vertex AI > Model Garden")
    print("2. 'Enable' the Gemini API / Model usage explicitly.")

if __name__ == "__main__":
    probe_regions()
