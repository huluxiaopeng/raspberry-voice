from aip import AipSpeech
import base64, requests
import json
import os
import pyaudio
import wave
import time
import RPi.GPIO as GPIO
from pyaudio import PyAudio,paInt16

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
framerate=16000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=8

ID= '15667585'
CUID = "hulu_play"
server = "https://openapi.baidu.com/oauth/2.0/token?"
grant_type = "client_credentials"
client_id = "WmqTNQvhzQKCW9woBeOzGtWi"
client_secret = "E4yFMs9k1lAb6PiCXWbtEUAVMrtxS1zi" 
url ="%sgrant_type=%s&client_id=%s&client_secret=%s"%(server,grant_type,client_id,client_secret)

while True:
    
    def get_token():       #获取token
        res = requests.post(url)
        token = json.loads(res.text)["access_token"]
        #print(token)
        return token


    def get_text():
        size = os.path.getsize('/home/pi/Desktop/filename/02.wav')
        with open(r'02.wav',"rb") as f :
            speech = base64.b64encode(f.read()).decode('utf8')

        d = open('02.wav', 'rb').read()
        data = {
            "format": "pcm",
            #"format": "wav",
            "rate": 16000,
            "channel": 1,
            "token": token,
            "cuid": CUID,
            "len": size,
            "speech": speech,
        }

        req = requests.post('http://vop.baidu.com/pro_api', json.dumps(data), headers={'Content-Type': 'application/json'})
        result = json.loads(req.text)
        wenzi = result['result'][0]
        print(wenzi)
        return wenzi

    def get_req():
        key = '366473177060436a9430c4f1873f42f3'
        userId = "huluzjp" 
        data = {
    # 请求的类型 0 文本 1 图片 2 音频
            "reqType": 0,
    # // 输入信息(必要参数)
            "perception": {
        # 文本信息
                "inputText": {
                    "text": wenzi
                }
            },
            "userInfo": {
                "apiKey": key,
                "userId": userId
            }
        }

        tuling_url = "http://openapi.tuling123.com/openapi/api/v2"
        res = requests.post(tuling_url,json=data)
    # 将返回信息解码
        res_dic = json.loads(res.content.decode("utf-8"))  # type:dict
    # 得到返回信息中的文本信息
        huifu = res_dic.get("results")[0].get("values").get("text")
        answer_message = json.loads(res.text)
        print(huifu)
        print(answer_message)
        return huifu
    
    def play():
        os.system('sox 01.mp3 01.wav')
        wf = wave.open('01.wav', 'rb')
        p = pyaudio.PyAudio()

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        stream.start_stream()

        while stream.is_active():
            time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        wf.close()

        p.terminate()
    while True:
        def save_wave_file(filename,data):
            wf=wave.open(filename,'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(framerate)
            wf.writeframes(b"".join(data))
            wf.close()
        def my_record():
            pa=PyAudio()
            stream=pa.open(format = paInt16,channels=1,
                           rate=framerate,input=True,
                           frames_per_buffer = NUM_SAMPLES)
            my_buf=[]
            count=0
            while count<TIME*5:#控制录音时间
                string_audio_data = stream.read(NUM_SAMPLES)
                my_buf.append(string_audio_data)
                count+=1
                print('.')
            save_wave_file('02.wav',my_buf)
            stream.close()
            pa.terminate()

        my_record()
        print('over')
        token = get_token()
        wenzi = get_text()
        client = AipSpeech(ID, client_id, client_secret)
        def v_c():
        
            if "开灯"in wenzi:
                GPIO.output(13, GPIO.HIGH)
                print("已为您开灯")
                result  = client.synthesis("已为您开灯", 'zh', 1, {
                'vol': 5, 'per': 4, })
                if not isinstance(result, dict):
                    with open('01.mp3','wb') as f:
                        f.write(result)
                    play()
            
            if "关灯" in wenzi:
                GPIO.output(13, GPIO.LOW)
                print("已为您关灯")
                result  = client.synthesis("已为您关灯", 'zh', 1, {
                'vol': 5, 'per': 4, })
                if not isinstance(result, dict):
                    with open('01.mp3','wb') as f:
                        f.write(result)
                    play()

            if "打开风扇"in wenzi:
                GPIO.output(15, GPIO.HIGH)
                print("已为您打开")
                result  = client.synthesis("已为您打开", 'zh', 1, {
                'vol': 5, 'per': 4, })
                if not isinstance(result, dict):
                    with open('01.mp3','wb') as f:
                        f.write(result)
                    play()

            if "关闭风扇"in wenzi:
                GPIO.output(15, GPIO.LOW)
                print("已为您关闭")
                result  = client.synthesis("已为您关闭", 'zh', 1, {
                'vol': 5, 'per': 4, })
                if not isinstance(result, dict):
                    with open('01.mp3','wb') as f:
                        f.write(result)
                    play()


            if "打开所有设备"in wenzi:
                GPIO.output(15, GPIO.HIGH)
                GPIO.output(13, GPIO.HIGH)
                print("已为您打开")
                result  = client.synthesis("已为您打开", 'zh', 1, {
                'vol': 5, 'per': 4, })
                if not isinstance(result, dict):
                    with open('01.mp3','wb') as f:
                        f.write(result)
                    play()


            if "关闭所有设备"in wenzi:
                GPIO.output(15, GPIO.LOW)
                GPIO.output(13, GPIO.LOW)
                print("已为您关闭")
                result  = client.synthesis("已为您关闭", 'zh', 1, {
                'vol': 5, 'per': 4, })
                if not isinstance(result, dict):
                    with open('01.mp3','wb') as f:
                        f.write(result)
                    play()

                    
        v_c()
        answer = get_req()
        result  = client.synthesis(answer, 'zh', 1, {
            'vol': 5, 'per': 4,
        })
        if not isinstance(result, dict):
            with open('01.mp3', 'wb') as f:
                f.write(result)
                play()
