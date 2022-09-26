# -*- ecoding: utf-8 -*-
# @ModuleName: download
# @Function: 
# @Author: qy
# @Time: 2022/2/24 16:48
import pygame
from aip import AipSpeech
import requests
import json
from django.http import HttpResponse, JsonResponse
import pyttsx3
from . import youdao_voice

# import youdao_voice

# 语音识别
APP_ID = '25553224'
API_KEY = 'R0eKeKmCprTP0PzTDK69m8uW'
SECRET_KEY = '2BelDodR7AZqG9TnVmk7GgjUMNfql1eP'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 调用图灵机器�?
TURING_KEY = "3519eaad5a5142fbbfd81838a53f1827"
URL = "http://openapi.tuling123.com/openapi/api/v2"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}


def robot(text=""):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": ""
            },
            "selfInfo": {
                "location": {
                    "city": "北京"
                }
            }
        },
        "userInfo": {
            "apiKey": 'abea0643e5f84cd9884e5caf9b46eb55',
            "userId": "123"
        }
    }

    data["perception"]["inputText"]["text"] = text
    response = requests.request("post", URL, json=data, headers=HEADERS)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    # print("the AI said: " + result)
    return result


# 语音合成
# tex	必填	合成的文本，使用UTF-8编码。小�?048个中文字或者英文数字。（文本在百度服务器内转换为GBK后，
# tok	必填	开放平台获取到的开发者access_token（见上面的“鉴权认证机制”段落）
# cuid	必填	用户唯一标识，用来计算UV值。建议填写能区分用户的机�?MAC 地址�?IMEI 码，长度�?0字符以内
# ctp	必填	客户端类型选择，web端填写固定�?
# lan	必填	固定值zh。语言选择,目前只有中英文混合模式，填写固定值zh
# spd	选填	语速，取�?-15，默认为5中语�?
# pit	选填	音调，取�?-15，默认为5中语�?
# vol	选填	音量，取�?-15，默认为5中音�?
# per	（基础音库�?选填 度小�?1，度小美=0，度逍遥=3，度丫丫=4
# per	（精品音库）	选填 度博�?106，度小童=110，度小萌=111，度米朵=103，度小娇=5
# aue	选填	3为mp3格式(默认)�?4为pcm-16k�?为pcm-8k�?为wav（内容同pcm-16k�? 注意aue=4或�?是语音识别要求的格式，但是音频内容不是语音识别要求的自然人发音，所以识别效果会受影响�?

def speak(text="", type="zh", name="audio.mp3"):
    result = client.synthesis(text, type, 1, {
        'spd': 4,
        'vol': 5,
        'per': 4,
    })

    if not isinstance(result, dict):
        with open(name, 'wb') as f:
            f.write(result)


# 播放音频
def play():
    pygame.mixer.init()
    pygame.mixer.music.load("audio.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.mixer.music.unload()


def pyttsx_api(text, name):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # 调整人声类型
    engine.setProperty('voice', voices[0].id)

    # 调整语�?范围一般在0~500之间
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 200)

    # 调整声量，范围在0~1之间
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 0.8)
    # 保存音频到本地，格式为mp3
    engine.save_to_file(text, name)
    engine.runAndWait()

    engine.save_to_file("text", ".mp3")
    engine.runAndWait()


def robot_api(request):
    # if request.method == 'POST':
    #     postBody = request.body
    #     request_json = json.loads(postBody)
    #     sentence = request_json['input_sentence']
    #     print(sentence)
    #     text_1 = robot(sentence)  # ��text�е����ַ��͸������ˣ����ػ����˵Ļظ��浽text_1
    #     pyttsx_api(text_1, './audio.mp3')
    #     return JsonResponse({'ret': 9, 'msg': '�ɹ�'})
    # elif request.method == "GET":
    #     with open('./audio.mp3', "rb") as f:
    #         c = f.read()
    #     return HttpResponse(c)
    # else:
    #     return JsonResponse({'ret': 1, 'msg': '�������'})
    print(request.POST)
    sentence = request.POST.get('input_sentence')
    print(sentence)
    text_1 = robot(sentence)  # ��text�е����ַ��͸������ˣ����ػ����˵Ļظ��浽text_1
    # pyttsx_api(text_1, './audio.mp3')
    return JsonResponse({'ret': 0, 'content': text_1})

    # if request.method == 'POST':
    #     postBody = request.body
    #     request_json = json.loads(postBody)
    #     sentence = request_json['input_sentence']
    #     print(sentence)
    #     text_1 = robot(sentence)  # ��text�е����ַ��͸������ˣ����ػ����˵Ļظ��浽text_1
    #     # pyttsx_api(text_1, './audio.mp3')
    #     return JsonResponse({'ret': 0, 'content': text_1})
    # # elif request.method == "GET":
    # #     with open('./audio.mp3', "rb") as f:
    # #         c = f.read()
    # #     return HttpResponse(c)
    # else:
    #     return JsonResponse({'ret': 1, 'msg': '�������'})


def download_file(request):
    if request.method == 'POST':
        postBody = request.body
        request_json = json.loads(postBody)
        sentence = request_json['input_sentence']
        print(sentence)
        # speak(sentence,type,name="example.mp3")  # 将text_1中机器人的回复用语音输出，保存为audio.mp3文件
        pyttsx_api(sentence, './test.mp3')
        return JsonResponse({'ret': 0, 'msg': sentence})
    elif request.method == "GET":
        with open('./test.mp3', "rb") as f:
            c = f.read()
        return HttpResponse(c)
    else:
        return JsonResponse({'ret': 1, 'msg': '请求错误'})


rote = ""


def get_word_voice(request):
    global rote
    if request.method == 'POST':
        postBody = request.body
        request_json = json.loads(postBody)
        sentence = request_json['input_word']
        type = request_json['type']
        sp = youdao_voice.youdao()
        sp.changeAccent(type)

        rote = sp.down(sentence)
        print(sentence, type)
        # speak(sentence,type,name="example.mp3")  # 将text_1中机器人的回复用语音输出，保存为audio.mp3文件
        return JsonResponse({'ret': 0, 'msg': sentence})
    elif request.method == "GET":
        print(rote)
        with open(rote, "rb") as f:
            c = f.read()
        return HttpResponse(c)
    else:
        return JsonResponse({'ret': 1, 'msg': '请求错误'})


if __name__ == "__main__":
    # while True:
    #     text = str(input("输入:"))
    #     if '结束程序' in text:  # 这里我设置了一个结束语，说“结束程序”的时候就结束，你也可以改�?
    #         break
    #     text_1 = robot(text)  # 将text中的文字发送给机器人，返回机器人的回复存到text_1
    #     speak(text_1)  # 将text_1中机器人的回复用语音输出，保存为audio.mp3文件
    #     play()  # 播放audio.mp3文件
    #
    #     pyttsx_api(text_1, "./mm.mp3")
    engine = pyttsx3.init()
    # 朗读音频保存

    pyttsx_api("11111", "mmm.mp3")
