from flask import Flask
import requests

app = Flask(__name__)

@app.route("/hello")
def hello_world():
    url = "https://api.aiforthai.in.th/partii-webapi"

    files = {'wavfile': ('test.wav', open('test.wav', 'rb'), 'audio/wav')}

    headers = {
        'Apikey': "wC353JjsGN0sKP6EUXoEeuvgsNDaLAxr",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
    }

    param = {"outputlevel": "--uttlevel", "outputformat": "--txt"}

    response = requests.request("POST", url, headers=headers, files=files, data=param)

    print("Result = " + response.text)
    return "<p>"+response.text+"</p>"