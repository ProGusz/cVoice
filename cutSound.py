from pydub import AudioSegment
import requests
import uuid
import os

def cut_audio2(input_file, output_file, second):
    """
    Cut parts of an audio file and save it to a new file.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the output audio file.
        start_time (int): Start time in milliseconds.
        end_time (int): End time in milliseconds.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    length = 1000 * second
    max_length = len(audio)
    print(max_length)

    out = []

    for start in range(0, max_length, length):
        # Cut the audio
        end = start + length
        print(start)
        cut = audio[start:end]
        cut = cut.set_frame_rate(16000)
        cut = cut.set_channels(1)

        out.append(output_file+str(start)+".wav")
        # Save the cut audio to a new file
        cut.export(output_file+str(start)+".wav", format="wav")
        #cut.export(output_file + str(start) + ".mp3", format="mp3")
        #subprocess.call(['ffmpeg', '-i', output_file+str(start)+".mp3",
        #                 output_file+str(start)+".wav"])

    return out


def cut_audio(input_file, output_file, start_time, end_time):
    """
    Cut parts of an audio file and save it to a new file.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the output audio file.
        start_time (int): Start time in milliseconds.
        end_time (int): End time in milliseconds.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    print(len(audio))

    # Cut the audio
    cut = audio[start_time:end_time]


    #cut.set_frame_rate(16000).set_channels(1)

    # Save the cut audio to a new file
    cut.export(output_file, format="mp3")


def convert(file):
    url = "https://api.aiforthai.in.th/partii-webapi"

    files = {'wavfile': (file, open(file, 'rb'), 'audio/wav')}

    headers = {
        'Apikey': "wC353JjsGN0sKP6EUXoEeuvgsNDaLAxr",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
    }

    param = {"outputlevel": "--uttlevel", "outputformat": "--txt"}

    response = requests.request("POST", url, headers=headers, files=files, data=param)

    print("Result = " + response.text)
    return "<p>"+response.text+"</p>"


# Example usage
#input_file = "E:\MyGit\pythonProject\pythonProject\sound.mp3"
#output_file = "E:\MyGit\pythonProject\pythonProject\\"+str(uuid.uuid4())

input_file = ".\sound.mp3"
output_file = ".\\"+str(uuid.uuid4())


print(output_file)

files = cut_audio2(input_file, output_file, 30)
print(files)
for i in files:
    print(i)
    #convert(i)
    os.remove(i)


