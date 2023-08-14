import openai
import requests
import json
import tempfile
import os
import speech_recognition as sr
from elevenlabs import clone, generate, play, set_api_key

# Set your OpenAI API key
openai.api_key = "open.api.key"

# Set your ElevenLabs API key
elevenlabs_api_key = "Eleven labs api key"
set_api_key(elevenlabs_api_key)

def text_to_speech(text, lang='en'):
    # Generate audio using ElevenLabs API
    audio = generate(
        text=text,
        voice="Charolette",
        model="eleven_monolingual_v1"
    )

    # Play the generated audio
    play(audio)

def main():
    input_mode = input("Choose input mode:\n1. Text\n2. Voice\n")
    
    if input_mode == "1":
        print("Using Text input mode.")
    elif input_mode == "2":
        print("Using Voice input mode.")
    else:
        print("Invalid input mode. Exiting the program.")
        return

    messages = []
    system_msg = "Personality"
    messages.append({"role": "system", "content": system_msg})

    print("Your tsundere assistant is ready!")

    while True:
        if input_mode == "1":
            user_message = input("You (Text): ")
            
        elif input_mode == "2":
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            with microphone as source:
                print("Speak:")
                audio = recognizer.listen(source)
            
            try:
                user_message = recognizer.recognize_google(audio)
                print("You (Voice):", user_message)
            except sr.UnknownValueError:
                print("Sorry, could not understand audio.")
            except sr.RequestError:
                print("Sorry, an error occurred while requesting audio.")
            except KeyboardInterrupt:
                print("Voice input interrupted.")
                continue
        
        if user_message.lower() == "quit":
            print("Exiting the chatbot.")
            break

        messages.append({"role": "user", "content": user_message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages)
        assistant_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": assistant_reply})

        print("\nAssistant:", assistant_reply)
        text_to_speech(assistant_reply, lang='en')  # Use English accent for speech

if __name__ == "__main__":
    main()

