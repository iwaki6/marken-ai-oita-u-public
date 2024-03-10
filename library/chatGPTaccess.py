import openai
from openai import OpenAI

client = OpenAI() # this needs environment variable 

def chat(system_role,prompt):
    try:
        # Make a request to OpenAI API for chat completion
        result = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages = [
                {"role": "system", "content": system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
    except openai.RateLimitError as e:
        return {"text":"Too much usage, please wait a moment.",
                "success":False
                }
    except openai.InternalServerError as e:
        return {"text":"The server is overloaded. Please wait a moment and try again.",
                "success":False
                }
    except openai.APIConnectionError as e:
        return {"text":"An error occurred during communication. Please wait a moment and try again.",
                "success":False
                }
    except openai._exceptions as e:
        return {"text":"An unexpected error has occurred. Please contact the support team for assistance.",
                "success":False
                }
    else:
        # Extract Assistant's response text
        return {"text":result.choices[0].message.content,
                "success":True
                }

def recognize(request):
    audio = request.files['audio']
    transcription = client.audio.transcriptions.create(
        model='whisper-1', 
        file=audio)
    return transcription.text
