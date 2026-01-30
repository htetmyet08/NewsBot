from content_processor import process_article
import config
import os

def test_vertex_connection():
    print("Testing Vertex AI Connection...")
    print(f"Project ID: {config.GCP_PROJECT_ID}")
    print(f"Location: {config.GCP_LOCATION}")
    print(f"Credentials: {config.GOOGLE_APPLICATION_CREDENTIALS}")

    if not config.GCP_PROJECT_ID:
        print("ERROR: GCP_PROJECT_ID is missing in .env")
        return

    if not config.GOOGLE_APPLICATION_CREDENTIALS or not os.path.exists(config.GOOGLE_APPLICATION_CREDENTIALS):
        print(f"WARNING: GOOGLE_APPLICATION_CREDENTIALS path seems invalid or file not found: {config.GOOGLE_APPLICATION_CREDENTIALS}")

    print("\nAttempting to process a dummy article...")
    title = "Test Article"
    description = "This is a test article to verify Vertex AI connectivity."
    
    my_title, my_summary = process_article(title, description, "http://example.com")
    
    if my_title or my_summary:
        print("\nSUCCESS! Received response from Vertex AI:")
        print(f"Title: {my_title}")
        print(f"Summary: {my_summary}")
    else:
        print("\nFAILURE: Did not receive a valid response. Check logs for details.")

if __name__ == "__main__":
    test_vertex_connection()
