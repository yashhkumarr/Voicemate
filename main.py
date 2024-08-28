import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import subprocess


openai.api_key = 'sk-...s-kA'

# Global variable to maintain chat history
Chatstr = ""

def text_to_speech(text):

    command = f"powershell -Command Add-Type –AssemblyName System.Speech; $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; $synth.Speak('{text}')"
    subprocess.run(command, shell=True)

def chat(query):
    """Generate a response from OpenAI's GPT-3/4 and provide a spoken output."""
    global Chatstr
    Chatstr += f"Yash: {query}\nVoiceMate: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=Chatstr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_text = response["choices"][0]["text"].strip()
        text_to_speech(response_text)
        Chatstr += f"{response_text}\n"
        return response_text
    except Exception as e:
        print(f"Error generating response: {e}")
        text_to_speech("Sorry, I encountered an error.")
        return "Sorry, something went wrong."

def ai(prompt):
    """Generate a response from OpenAI's GPT-3/4 and save it to a file."""
    try:
        text = f"OpenAI response for Prompt: {prompt}\n*************************\n\n"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response["choices"][0]["text"].strip()
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        file_name = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        with open(file_name, "w") as f:
            f.write(text)
    except Exception as e:
        print(f"Error saving AI response: {e}")

def say(text):
    """Use text-to-speech command compatible with the OS."""
    if os.name == 'nt':  # Windows
        text_to_speech(text)
    else:  # For Unix-like systems
        subprocess.run(f"say {text}", shell=True)

def take_command():
    """Listen to the user's voice input and convert it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=10)  # Increased timeout to 10 seconds
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return ""

def open_website(site_name, url):
    """Open a website."""
    say(f"Opening {site_name} for you...")
    webbrowser.open(url)

def main():
    """Main function to run the voice assistant."""
    print("Welcome to VOICEMATE")
    say("Welcome To VOICE MATE")

    while True:
        print("Listening...")
        query = take_command()
        if not query:
            continue

        query_lower = query.lower()

        # Handle various commands and responses
        if "hello" in query_lower:
            response = "Hello! How can I assist you today?"
            say(response)

        elif "how are you today" in query_lower:
            response = "I'm doing well, thank you! How can I help you?"
            say(response)

        elif any(f"open {site[0]}".lower() in query_lower for site in
                 [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                  ["google", "https://www.google.com"], ["facebook", "https://www.facebook.com"],
                  ["instagram", "https://www.instagram.com"], ["amizone", "https://s.amizone.net"],
                  ["amazon", "https://www.amazon.com"], ["whatsapp", "https://web.whatsapp.com"]]):
            for site in [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                         ["google", "https://www.google.com"], ["facebook", "https://www.facebook.com"],
                         ["instagram", "https://www.instagram.com"], ["amizone", "https://s.amizone.net"],
                         ["amazon", "https://www.amazon.com"], ["whatsapp", "https://web.whatsapp.com"]]:
                if f"open {site[0]}".lower() in query_lower:
                    open_website(site[0], site[1])

        elif "close browser" in query_lower or "close website" in query_lower:
            say("Closing the browser.")
            os.system("taskkill /IM chrome.exe /F")

        elif "open notepad" in query_lower:
            if os.name == 'nt':  # Windows
                os.system("notepad")
            else:
                say("Sorry, opening Notepad is not supported on this operating system.")

        elif "open music" in query_lower:
            music_path = "C:\\ Users\\yashk\\Music\\YourMusicFile.mp3"  # Update this path as needed
            os.startfile(music_path)

        elif "the time" in query_lower:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The time is {hour} hours and {minute} minutes.")

        elif "which day is today" in query_lower:
            day = datetime.datetime.now().strftime("%A")
            say(f"Today is {day}.")

        elif "what will be the day tomorrow" in query_lower:
            tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%A")
            say(f"Tomorrow will be {tomorrow}.")

        elif "what date is today" in query_lower:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            say(f"Today's date is {date}.")

        elif "open camera" in query_lower:
            if os.name == 'nt':  # Windows
                os.system("start microsoft.windows.camera:")
            else:
                say("Sorry, opening the camera is not supported on this operating system.")

        elif "open file explorer" in query_lower:
            if os.name == 'nt':  # Windows
                os.system("explorer")
            else:
                say("Sorry, opening File Explorer is not supported on this operating system.")

        elif "using artificial intelligence" in query_lower:
            ai(prompt=query)

        elif "quit" in query_lower:
            say("Goodbye!")
            break

        elif "reset chat" in query_lower:
            global Chatstr
            Chatstr = ""
            say("Chat reset.")

        else:
            print("Chatting...")
            response = chat(query)

        # Ask if it can assist with anything else
        say("Can I assist you with anything else?")

if __name__ == '__main__':
    main()
