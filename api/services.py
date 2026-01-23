import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Prompt Engineering based on PRD Section 3.1
PROMPTS = {
    "ko": {
        "boss": {
            "role": "You are a professional assistant communicating with a boss.",
            "instruction": (
                "Convert the following text into a formal report format suitable for a boss. "
                "Tone: Polite, formal, trustworthy, and authoritative. "
                "Style: Start with the conclusion or key point clearly. Use '습니다/합니다' endings. "
                "Output ONLY the converted Korean text without any explanation."
            )
        },
        "colleague": {
            "role": "You are a helpful and respectful team member.",
            "instruction": (
                "Convert the following text into a friendly yet professional message for a coworker. "
                "Tone: Polite (using '해요' style), mutual respect, cooperative. "
                "Style: Clearly state requests and deadlines. "
                "Output ONLY the converted Korean text without any explanation."
            )
        },
        "customer": {
            "role": "You are a professional customer service representative.",
            "instruction": (
                "Convert the following text into an extremely polite and service-oriented message for a customer. "
                "Tone: Honorifics (extreme politeness), professional, empathetic. "
                "Style: Emphasize service mindset, use '안녕하십니까', '감사합니다' etc. "
                "Output ONLY the converted Korean text without any explanation."
            )
        }
    },
    "en": {
        "boss": {
            "role": "You are a professional executive assistant.",
            "instruction": (
                "Convert the following text into a professional and formal business message for a superior. "
                "Tone: Formal, concise, respectful, and professional. "
                "Style: Use standard business English (e.g., 'I am writing to inform you...', 'Please let me know if...'). "
                "Output ONLY the converted English text without any explanation."
            )
        },
        "colleague": {
            "role": "You are a collaborative team member.",
            "instruction": (
                "Convert the following text into a polite and professional message for a colleague. "
                "Tone: Friendly, professional, and clear. "
                "Style: Semi-formal business English. Be direct but respectful. "
                "Output ONLY the converted English text without any explanation."
            )
        },
        "customer": {
            "role": "You are a highly professional customer relations manager.",
            "instruction": (
                "Convert the following text into a very polite and professional customer service message. "
                "Tone: Courteous, helpful, and formal. "
                "Style: Polished business English (e.g., 'Thank you for contacting us', 'We appreciate your patience'). "
                "Output ONLY the converted English text without any explanation."
            )
        }
    }
}

def convert_text(text: str, target: str, lang: str = "ko") -> str:
    """
    Converts text to business tone based on the target audience and language using Groq API.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    # Select language prompts
    lang_prompts = PROMPTS.get(lang, PROMPTS["ko"])
    
    # Select prompt based on target, default to 'colleague'
    prompt_config = lang_prompts.get(target, lang_prompts["colleague"])

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": f"{prompt_config['role']} {prompt_config['instruction']}"
            },
            {
                "role": "user", 
                "content": text
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        converted_text = data['choices'][0]['message']['content'].strip()
        
        if converted_text.startswith('"') and converted_text.endswith('"'):
            converted_text = converted_text[1:-1]
            
        return converted_text

    except requests.exceptions.RequestException as e:
        print(f"Groq API Request Error: {e}")
        raise Exception("Failed to communicate with AI service.")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Response Parsing Error: {e}")
        raise Exception("Failed to process AI response.")