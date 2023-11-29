from pydub import AudioSegment
import requests
import uuid
import os
from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

@app.route('/')
def main():
    #return render_template("index.html")
    return render_template('template.html', description='')

@app.route("/oh_my_teacher", methods=['POST'])
def oh_my_teacher():
    filename = ""
    caption = ""
    summary_caption = ""

    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)

        filename = f.filename

        input_file = ".\\" + f.filename
        output_file = ".\\" + str(uuid.uuid4())

        print(output_file)

        files = cut_audio(input_file, output_file, 30)
        print(files)

        desc = ""
        for i in files:
            print(i)
            desc += " " + convert(i)
            os.remove(i)

        caption = desc
        #caption = desc.replace(" ","")

        summary_caption = summary(caption)

    os.remove(".\\"+filename)
    data = {
        "file": filename,
        "caption": caption,
        "summary": summary_caption,
    }

    #return jsonify(data)
    return render_template('template.html', caption=caption, summary=summary_caption)


def cut_audio(_input_file, _output_file, second):
    """
    Cut parts of an audio file and save it to a new file.

    Args:
        _input_file (str): Path to the input audio file.
        _output_file (str): Path to save the output audio file.
        second (int): time in second to be cut.
    """
    # Load the audio file
    audio = AudioSegment.from_file(_input_file)

    # max audio length
    length = 1000 * second
    max_length = len(audio)

    # files return
    return_files = []
    for start in range(0, max_length, length):
        # Cut the audio
        end = start + length
        print(start)
        cut = audio[start:end]
        cut = cut.set_frame_rate(16000)
        cut = cut.set_channels(1)

        return_files.append(_output_file + str(start) + ".wav")
        # Save the cut audio to a new file
        cut.export(_output_file + str(start) + ".wav", format="wav")

    return return_files

def summary(caption):
    #caption = "ข้าว เป็นเมล็ดของพืชหญ้า Oryza sativa (ชื่อสามัญ: ข้าวเอเชีย) ที่พบมากในทวีปเอเชีย ข้าวเป็นธัญพืชซึ่งประชากรโลกบริโภคเป็นอาหารสำคัญ โดยเฉพาะอย่างยิ่งในทวีปเอเชีย จากข้อมูลเมื่อปี 2553 ข้าวเป็นธัญพืชซึ่งมีการปลูกมากที่สุดเป็นอันดับสามทั่วโลก รองจากข้าวสาลีและข้าวโพด ข้าวเป็นธัญพืชสำคัญที่สุดในด้านโภชนาการและการได้รับแคลอรีของมนุษย์ เพราะข้าวโพดส่วนใหญ่ปลูกเพื่อจุดประสงค์อื่น มิใช่ให้มนุษย์บริโภค ทั้งนี้ ข้าวคิดเป็นพลังงานกว่าหนึ่งในห้าที่มนุษย์ทั่วโลกบริโภค หลักฐานพันธุศาสตร์แสดงว่าข้าวมาจากการนำมาปลูกเมื่อราว 8,200–13,500 ปีก่อน ในภูมิภาคหุบแม่น้ำจูเจียงของจีน ก่อนหน้านี้ หลักฐานโบราณคดีเสนอว่า ข้าวมีการนำมาปลูกในเขตหุบแม่น้ำแยงซีในจีน ข้าวแพร่กระจายจากเอเชียตะวันออกไปยังเอเชียตะวันออกเฉียงใต้และเอเชียใต้ ข้าวถูกนำมายังทวีปยุโรปผ่านเอเชียตะวันตก และทวีปอเมริกาผ่านการยึดอาณานิคมของยุโรป[3] ปกติการปลูกข้าวเป็นแบบปีต่อปี ทว่าในเขตร้อน ข้าวสามารถมีชีวิตอยู่ได้หลายปีและสามารถไว้ตอ (ratoon) ได้นานถึง 30 ปี ต้นข้าวสามารถโตได้ถึง 1–1.8 เมตร ขึ้นอยู่กับพันธุ์และความอุดมสมบูรณ์ของดินเป็นหลัก มีใบเรียว ยาว 50-100 เซนติเมตร และกว้าง 2-2.5 เซนติเมตร ช่อดอกห้อยยาว 30-50 เซนติเมตร เมล็ดกินได้เป็นผลธัญพืชยาว 5-12 มิลลิเมตร และหนา 2-3 มิลลิเมตร การเตรียมดินสำหรับเพาะปลูกข้าวเหมาะกับประเทศและภูมิภาคที่ค่าแรงต่ำและฝนตกมาก เนื่องจากมันใช้แรงงานมากที่จะเตรียมดินและต้องการน้ำเพียงพอ อย่างไรก็ตาม ข้าวสามารถโตได้เกือบทุกที่ แม้บนเนินชันหรือเขตภูเขาที่ใช้ระบบควบคุมน้ำแบบขั้นบันได แม้ว่าสปีชีส์บุพการีของมันเป็นสิ่งพื้นเมืองของเอเชียและส่วนที่แน่นอนของแอฟริกา ร้อยปีของการค้าขายและการส่งออกทำให้มันสามัญในหลายวัฒนธรรมทั่วโลก วิธีแบบดั้งเดิมสำหรับเตรียมดินสำหรับข้าวคือทำให้น้ำท่วมแปลงชั่วขณะหนึ่งหรือหลังจากการตั้งของต้นกล้าอายุน้อย วิธีเรียบง่ายนี้ต้องการการวางแผนที่แข็งแรงและการให้บริการของเขื่อนและร่องน้ำ แต่ลดพัฒนาการของเมล็ดที่ไม่ค่อยแข็งแรงและวัชพืชที่ไม่มีภาวะเติบโตขณะจมน้ำ และยับยั้งศัตรูพืช ขณะที่การทำให้น้ำท่วมไม่จำเป็นสำหรับการเตรียมดินสำหรับเพาะปลูกข้าว วิธีทั้งหมดในการชลประทานต้องการความพยายามสูงกว่าในการควบคุมวัชพืชและศัตรูพืชระหว่างช่วงเวลาการเจริญเติบโตและวิธีที่แตกต่างสำหรับใส่ปุ๋ยลงดิน"
    url = 'https://api.aiforthai.in.th/textsummarize'

    headers = {'Apikey': 'wC353JjsGN0sKP6EUXoEeuvgsNDaLAxr', 'Content-Type': 'application/json'}

    params = json.dumps([{"id": 100, "comp_rate": 30,
                          "src": caption}])

    response = requests.post(url, data=params, headers=headers)

    # convert string to  object
    json_object = json.loads(response.text)

    print(type(json_object))

    print(json_object)

    return json_object #json_object["message"]


def convert(file):
    url = "https://api.aiforthai.in.th/partii-webapi"

    _files = {'wavfile': (file, open(file, 'rb'), 'audio/wav')}

    headers = {
        'Apikey': "wC353JjsGN0sKP6EUXoEeuvgsNDaLAxr",
        'Cache-Control': "no-cache",
        'Connection': "keep-alive",
    }

    param = {"outputlevel": "--uttlevel", "outputformat": "--txt"}

    response = requests.request("POST", url, headers=headers, files=_files, data=param)

    # convert string to  object
    json_object = json.loads(response.text)

    print(type(json_object))
    print(json_object["message"])
    return json_object["message"]


# Main Program
"""
input_file = ".\sound.mp3"
output_file = ".\\" + str(uuid.uuid4())

print(output_file)

files = cut_audio(input_file, output_file, 30)
print(files)
for i in files:
    print(i)
    # convert(i)
    os.remove(i)
"""

if __name__ == '__main__':
    app.run(debug=True)
