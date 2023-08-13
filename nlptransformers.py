import openai
from gtts import gTTS
import playsound
import tempfile
import os
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = "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"

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio_file:
        temp_audio_filename = temp_audio_file.name
        tts.save(temp_audio_filename)

    playsound.playsound(temp_audio_filename, True)
    os.remove(temp_audio_filename)

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
    system_msg = "You are a short tempered girl assistant."  # Set the tsundere personality
    messages.append({"role": "system", "content": system_msg})

    print("Your assistant is ready!")

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
        text_to_speech(assistant_reply, lang='en')  # Use Jp accent for speech

if __name__ == "__main__":
    main()

