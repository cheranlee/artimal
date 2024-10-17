#This code implements code_1.py using MySQl database.

# import libraries 
from openai import OpenAI 
import sqlite3     # change to mysql 
import mysql.connector as mysql
import sounddevice as sd 
import soundfile as sf 
from scipy.io.wavfile import write 
from pathlib import Path 
# 9/10 start add rec time - Reb
import time
import sys
# 9/10 end add rec time - Reb
import os
from dotenv import load_dotenv # to load the env file 10/16 Aditya
load_dotenv() # to load the env file 10/16 Aditya

#setup mysql connection. - 10/15 Aditya
connection = mysql.connect( 
    host = os.getenv('MYSQL_HOST'), 
    port = int(os.getenv('MYSQL_PORT')),
    user = os.getenv('MYSQL_USER'),
    database = os.getenv('MYSQL_DATABASE'),
    password = os.getenv('MYSQL_PASSWORD')
)
cursor = connection.cursor()

# function to get openai's reply 
def get_openai_reply(client, role_message, prompt_message):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": role_message},  
        {"role": "user", "content": prompt_message}
    ]
    )
    reply_message = completion.choices[0].message.content
    return completion, reply_message

# function to get text to speech 
def get_audio_reply(client, reply_message): 
    with client.audio.speech.with_streaming_response.create(
        model="tts-1", 
        voice = "alloy", 
        input=reply_message
        ) as response: 
        response.stream_to_file("recordings/output/speech.wav")

def main(): 
    print("Pick an Option: \n\t1) Choose a Question from a set list \n\t2) Ask a new question \n\t3) Quit Program")

    # connect to openai 
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    choice = int(input("What is your choice? (1, 2, 3) "))
    # 8/10 end change input text - Reb

    while choice != 3: # handles invalid inputs because it only execute valid inputs
        if choice == 2:
            # record qn's audio file 
            fs = 44100  # Sample rate
            seconds = 10  # Duration of recording
            print("Ask Otter a Question!")
            # 9/10 end - reb
            myrecording = sd.rec(
                frames = int(seconds * fs), 
                samplerate=fs, 
                channels=1)

            # 9/10 start add rec time - Reb
            start_time = time.time()

            # Loop to print elapsed time every second, overwriting previous print
            while time.time() - start_time <= seconds:
                time.sleep(1)
                elapsed_time = time.time() - start_time
                sys.stdout.write(f"\rrecording in progress... {int(elapsed_time)}/10 seconds")
                sys.stdout.flush() #ensures overwritten text is immediately visible
            # 9/10 end add rec time - Reb

            sd.wait()  # Wait until recording is finished

            # 9/10 start add rec time - Reb
            #print("recording ends")
            # 9/10 end add rec time - Reb

            write('recordings/input/recorded_input.wav', fs, myrecording)  # Save as WAV file 

            # transcribe audio file into text 

            with open("recordings/input/recorded_input.wav", "rb") as audio_file: 
                transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
                )
            prompt_message = transcript.text
            
            # 9/10 start - reb
            sys.stdout.write(f"\rUser: {prompt_message}                                                       \n")
            sys.stdout.flush()
            #print(prompt_message)
            # 9/10 end - reb

            # play file to test 
            filename = 'recordings/input/recorded_input.wav'
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs) 

            # 9/10 start - reb
            start_time = time.time()
            duration = len(data) / fs  # Calculate the duration of the audio in seconds

            # Loop to print elapsed time every second, overwriting the previous print
            while time.time() - start_time <= duration:
                time.sleep(1)
                elapsed_time = time.time() - start_time
                sys.stdout.write(f"\rPlaying audio... {int(elapsed_time)}/10 seconds                                              ")
                sys.stdout.flush()
            # 9/10 end -reb
            status = sd.wait() 

            # 9/10 start - reb
            #sys.stdout.write(f"\rAudio playback finished                       ")
            # 9/10 end - reb

            # get openai's written reply 
            role_message = "You are an Otter. Reply in Otter English"
            completion, reply_message = get_openai_reply(client, role_message, prompt_message)

            # 9/10 start - reb
            sys.stdout.write(f"\rOpenAI's reply: {reply_message}                                                      \n")
            sys.stdout.flush()
            #print("OpenAI's reply: ", reply_message)
            # 9/10 end - reb

            # add to sql database 
            input_prompt = "INSERT INTO Otter(Question, Answer) VALUES(%s, %s)"
            cursor.execute(input_prompt, (prompt_message, reply_message))  
            connection.commit()
            cursor.reset()

            # convert openai's written reply to audio and play the audio 
            get_audio_reply(client, reply_message) 
            filename = 'recordings/output/speech.wav'
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs) 
            status = sd.wait() 
 
        elif choice == 1: 
                qn_keyword = str(input("question keywords: "))
                lower_qn_keyword = qn_keyword.lower()
                query = "%" + lower_qn_keyword + "%"
                cursor.execute("SELECT Answer FROM Otter WHERE Question LIKE %s", (query, ))
                result = cursor.fetchone() 
                cursor.reset()  
                print(result) 
                if result: 
                    get_audio_reply(client, result[0])
                    filename = 'recordings/output/speech.wav'
                    data, fs = sf.read(filename, dtype='float32')
                    sd.play(data, fs) 
                    status = sd.wait() 
                    # 10/10 start remove print statement- Reb
                    #print('test')
                    # 10/10 end remove print statement - Reb
                    
        print("Pick an Option: \n\t1) Choose a Question from a set list \n\t2) Ask a new question \n\t3) Quit Program")
        
        # 8/10 start change input text - Reb
        #choice = int(input("What is your choice? (1, 2, 3)"))
        choice = int(input("What is your choice? (1, 2, 3) "))
        # 8/10 end change input text - Reb

    print("EXIT PROGRAM")

