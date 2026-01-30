from google import genai
import config

def get_gemini_client():
    if not config.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is not set.")
        return None
    return genai.Client(api_key=config.GEMINI_API_KEY)

def process_article(title, description, url):
    """
    Rewrites the news title and description into Myanmar language using Gemini.
    """
    client = get_gemini_client()
    if not client:
        return None, None

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
        response = client.models.generate_content(
            model='gemini-1.5-flash-001',
            contents=prompt
        )
        text = response.text
        
        # Simple parsing logic (assuming Gemini follows the format)
        lines = text.strip().split('\n')
        my_title = ""
        my_summary = ""
        
        for line in lines:
            if line.startswith("Title:"):
                my_title = line.replace("Title:", "").strip()
            elif line.startswith("Summary:"):
                my_summary = line.replace("Summary:", "").strip()
        
        # Fallback if parsing fails but text exists
        if not my_title and not my_summary and text:
             my_summary = text

        return my_title, my_summary

    except Exception as e:
        print(f"Error processing content with Gemini: {e}")
        return None, None
