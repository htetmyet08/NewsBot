import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
import config

def init_vertex_ai():
    if not config.GCP_PROJECT_ID:
        print("Error: GCP_PROJECT_ID is not set.")
        return False
    
    try:
        vertexai.init(project=config.GCP_PROJECT_ID, location=config.GCP_LOCATION)
        return True
    except Exception as e:
        print(f"Error initializing Vertex AI: {e}")
        return False

def process_article(title, description, url):
    """
    Rewrites the news title and description into Myanmar language using Vertex AI Gemini Flash.
    """
    if not init_vertex_ai():
        return None, None

    model = GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are a professional news translator and editor.
    Translate the following news title and description into natural-sounding Myanmar language (Burmese).
    The tone should be formal and informative, suitable for a news broadcast.
    
    News Title: {title}
    News Description: {description}
    
    Output Format:
    Title: [Myanmar Title]
    Summary: [Myanmar Summary]
    """

    try:
        logging_level = "WARNING" # Reduce spam
        
        # Generation config
        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 0.2,
            "top_p": 0.95,
        }

        safety_settings = [
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
            ),
        ]

        responses = model.generate_content(
            [prompt],
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False,
        )

        text = responses.text
        
        # Simple parsing logic
        lines = text.strip().split('\n')
        my_title = ""
        my_summary = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith("Title:") or line.startswith("**Title:**"):
                my_title = line.split(":", 1)[1].strip().replace("*", "")
            elif line.startswith("Summary:") or line.startswith("**Summary:**"):
                my_summary = line.split(":", 1)[1].strip().replace("*", "")
        
        # Fallback if parsing fails but text exists
        if not my_title and not my_summary and text:
             my_summary = text

        return my_title, my_summary

    except Exception as e:
        print(f"Error processing content with Vertex AI: {e}")
        return None, None

