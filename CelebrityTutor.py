import requests
import re
import json
import args
import datetime
import os
from RealtimeTTS import TextToAudioStream, CoquiEngine

def getResponse(api_key: str,
                prompt: str, 
                model: str = "openai/gpt-3.5-turbo",
                temperature: float = 1.0,
                top_p: float = 1.0,
                top_k: int = 0,
                frequency_penalty: float = 0.0,
                presence_penalty: float = 0.0,
                repetition_penalty: float = 1.0,
                min_p: float = 0.0,
                top_a: float = 0.0,
                seed: int = None,
                max_tokens: int = None):
        """This function takes a prompt and optional parameters, such as model, and returns a json response from the model.

        Args:
            prompt (str): The prompt to send to the model.
            model (str, optional): The model to use. Defaults to "openai/gpt-3.5-turbo".
            temperature (float, optional): The temperature to use. Defaults to 1.0, can be 0.0 to 2.0.
            top_p (float, optional): The top_p to use. Defaults to 1.0, can be 0.0 to 1.0.
            top_k (int, optional): The top_k to use. Defaults to 0, can be 0 or above.
            frequency_penalty (float, optional): The frequency_penalty to use. Defaults to 0.0, can be -2.0 to 2.0.
            presence_penalty (float, optional): The presence_penalty to use. Defaults to 0.0, can be -2.0 to 2.0.
            repetition_penalty (float, optional): The repetition_penalty to use. Defaults to 1.0, can be 0.0 to 2.0.
            min_p (float, optional): The min_p to use. Defaults to 0.0, can be 0.0 to 1.0.
            top_a (float, optional): The top_a to use. Defaults to 0.0, can be 0.0 to 1.0.
            seed (int, optional): The seed to use. Defaults to None.
            max_tokens (int, optional): The max_tokens to use. Defaults to None.

        Returns:
            response.json(): The json response from the model.

        Note:
            For full details on all the parameters, visit https://openrouter.ai/docs/parameters
        
        """

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/RyderSwanson/CelebrityTutor",
                "X-Title": "CelebrityTutor",
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
                "repetition_penalty": repetition_penalty,
                "min_p": min_p,
                "top_a": top_a,
                "seed": seed,
                "max_tokens": max_tokens
            })
        )

        response = response.json()

        return response

def remove_markdown(text):
    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`.*?`', '', text)
    # Remove headers
    text = re.sub(r'#+ ', '', text)
    # Remove links
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    # Remove images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove bold and italic
    text = re.sub(r'\*\*|__|\*|_', '', text)
    # Remove blockquotes
    text = re.sub(r'> ', '', text)
    # Remove horizontal rules
    text = re.sub(r'---', '', text)
    return text

def get_lecture():
    with open(f"prompts/{args.prompt}", "r", encoding="utf-8") as file:
        prompt = file.read()
    response = getResponse(args.api_key, prompt, "google/gemini-flash-1.5-8b")

    try:
        message = response['choices'][0]['message']['content']
    except KeyError:
        print("The message could not be found. Here is the response:\n")
        print(response)
        exit()

    message = remove_markdown(message)
    return message

if __name__ == "__main__":
    engine = CoquiEngine(voice=f"voices/{args.voice}", full_sentences=True)

    again = True

    while again:
        message = get_lecture()

        output_dir = f"history/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}/"
        os.makedirs(os.path.dirname(output_dir), exist_ok=True)

        # Save message to file
        with open(f"{output_dir}lecture.txt", "w", encoding="utf-8") as file:
            file.write(message)

        TextToAudioStream(engine).feed([message]).play(output_wavfile=f"{output_dir}lecture.wav")

        again = input("Would you like to generate another lecture? (y/n) ").lower() == "y"

    engine.shutdown()

