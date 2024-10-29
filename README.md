# CelebrityTutor

## Project Summary
Tired of passively reading study materials?  CelebrityTutor revolutionizes your learning experience by transforming text into engaging, personalized audio.  Simply provide a prompt, and this tool will:

1. Intelligent Querying: Leverage the power of your chosen Large Language Model (LLM) to generate insightful and comprehensive responses to your study prompt.

2. Real-time Voice Synthesis:  Transform the LLM's output into natural-sounding speech, employing a voice style replicated from a 30-second sample you provide.  Experience the convenience of customized audio learning.

3. Effortless Organization:  Automatically save both the generated audio file and the original LLM response for easy access and review.  All your study materials are neatly organized in a dedicated folder.

## Installation

### Setup

1. Clone this repo onto your computer: ```git clone https://github.com/RyderSwanson/CelebrityTutor.git```
2. Install python dependencies: ```pip install -r requirements.txt```
3. Add your OpenRouter api key to the ```args.py``` file
    * You can obtain an api key at [OpenRouter](https://openrouter.ai/settings/keys)
        * I reccomend setting a credit limit, just in case your key gets compromised.
4. Create a new text file to contain your prompt in ./prompts
5. Go back to the ```args.py``` file and modify the "prompt" variable to the name of your new prompt file, for example: ```prompt = "MyCoolPrompt.txt"```


### Usage

To use CelebrityTutor all you need to do is run ```CelebrityTutor.py```. This can be done by simply double clicking on the file (assuming python is associated with .py files) or by running the following command in a terminal opened in the root folder of CelebrityTutor: ```python CelebrityTutor.py```


### Add a custom voice

1. Obtain an audio clip of the voice you want and save this as a ```.wav``` file
2. Place this file in the voices directory
3. Open ```args.py``` and modify the "voice" variable to reflect the file name of your audio clip, for example: ```voice = "JordanPeterson.wav"```
4. Simply run as you usually would and the voice should start working immedietly
    * Note: The first time you run a new voice a short training period will happen (Usually around ~10 seconds)
