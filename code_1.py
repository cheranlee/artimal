# import libraries 
from openai import OpenAI 
import sqlite3     # change to mysql 
import sounddevice as sd 
import soundfile as sf 
from scipy.io.wavfile import write 
from pathlib import Path 

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
        response.stream_to_file("speech.wav")

def main(): 
    print("Pick an Option: \n\t1) Choose a Question from a set list \n\t2) Ask a new question \n\t3) Quit Program")

    # connect to openai 
    api_key = ""
    client = OpenAI(
    api_key=api_key,
    )

    choice = int(input("What is your choice? (1, 2, 3)"))
    while choice != 3: 
        if choice == 2:
            # record qn's audio file 
            fs = 44100  # Sample rate
            seconds = 10  # Duration of recording
            print("Ask Otter a Question! recording starts")
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            print("recording ends")
            write('output.wav', fs, myrecording)  # Save as WAV file 

            # play file to test 
            filename = 'output.wav'
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs) 
            status = sd.wait() 

            # transcribe audio file into text 

            with open("output.wav", "rb") as audio_file: 
                transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
                )
            prompt_message = transcript.text
            print(prompt_message)

            # get openai's written reply 
            role_message = "You are an Otter. Reply in Otter English"
            completion, reply_message = get_openai_reply(client, role_message, prompt_message)

            print("OpenAI's reply: ", reply_message)

            # add to sql database 
            with sqlite3.connect("artimal.db") as connection: 
                connection.execute("INSERT INTO Otter(Question, Answer) \
                                VALUES(?, ?)", (prompt_message, reply_message))
                connection.commit() 

            # convert openai's written reply to audio and play the audio 
            get_audio_reply(client, reply_message) 
            filename = 'speech.wav'
            data, fs = sf.read(filename, dtype='float32')
            sd.play(data, fs) 
            status = sd.wait() 
 
        elif choice == 1: 
            with sqlite3.connect("artimal.db") as connection:
                    cur = connection.cursor() 
                    qn_keyword = str(input("question keywords: "))
                    lower_qn_keyword = qn_keyword.lower()
                    query = "%" + lower_qn_keyword + "%"
                    cur.execute("SELECT Question, Answer FROM Otter WHERE Question LIKE ?", (query, ))
                    rows = cur.fetchone() 
                    print(rows) 
                    if rows: 
                        print(rows[1])
                        get_audio_reply(client, rows[1])
                        filename = 'speech.wav'
                        data, fs = sf.read(filename, dtype='float32')
                        sd.play(data, fs) 
                        status = sd.wait() 
                        print('test')
                    cur.close() 
        print("Pick an Option: \n\t1) Choose a Question from a set list \n\t2) Ask a new question \n\t3) Quit Program")
        choice = int(input("What is your choice? (1, 2, 3)"))
    print("EXIT PROGRAM")

main() 
