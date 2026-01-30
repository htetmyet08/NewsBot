import google.generativeai as genai
import config

def configure_gemini():
    if not config.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is not set.")
        return False
    genai.configure(api_key=config.GEMINI_API_KEY)
    return True

def process_article(title, description, url):
    """
    Rewrites the news title and description into Myanmar language using Gemini.
    """
    if not configure_gemini():
        return None, None

    model = genai.GenerativeModel('gemini-1.5-flash')

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
        response = model.generate_content(prompt)
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
