import base64
import json
from django.http import HttpResponse, JsonResponse
import numpy as np
import cv2
import io
from PIL import Image
import time
import cv2
import numpy as np
import logging

from kernel.process.mode_processor import ModeProcessor
from api.youdao_word import Youdao_EtoZ, Youdao_ZtoE
from api.youdao_sentence import Sentence
from api.baidu_dict import Baidu
import time

from api.models import Query, User, Time

process = ModeProcessor(device="GPU")  # device="GPU" or "CPU"


def get_result_text(mode, api_results):
    result_text = ""
    if mode == 0:
        if api_results[1]['ret'] == 0:
            result_text += "拼音：" + api_results[1]['relist']['拼音'][0] + "\n"
            result_text += "释义：" + api_results[1]['relist']['基本释义'] + "\n"
        else:
            result_text += "拼音：" + "none \n"
            result_text += "释义：" + "none \n"
    if mode == 1:
        if api_results[1]['ret'] == 0:
            result_text += "拼音：" + api_results[1]['relist']['拼音'][0] + "\n"
            result_text += "释义：" + api_results[1]['relist']['基本释义'] + "\n"
            result_text += "近义词：" + api_results[1]['relist']['近义词'] + "\n"
            result_text += "反义词：" + api_results[1]['relist']['反义词'] + "\n"
        if api_results[0]['ret'] == 0:
            result_text += "英文：" + api_results[0]['relist']['英文'] + "\n"
            result_text += "英标：" + api_results[0]['relist']['英标'] + "\n"
    if mode == 2:
        if api_results[0]['ret'] == 0:
            result_text += "翻译：" + api_results[0]['relist'] + "\n"
    if mode == 3:
        if api_results[0]['ret'] == 0:
            result_text += "英文：" + api_results[0]['relist']['英文'] + "\n"
            result_text += "释义：" + api_results[0]['relist']['释义'] + "\n"
    return result_text


def test(request):
    src = request.POST.get('imgData')
    mode = int(request.POST.get('mode'))
    xl = request.POST.get('xl')
    yl = request.POST.get('yl')
    xr = request.POST.get('xr')
    yr = request.POST.get('yr')
    userid = request.POST.get('usrid')

    timeStamp = time.time()
    localTime = time.localtime(timeStamp)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)

    data = src.split(',')[1]
    image_data = base64.b64decode(data)

    image_np = np.frombuffer(image_data, dtype=np.uint8)
    image_np = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    # img_np_arr = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    text_results = ""

    try:
        finger_coord1 = np.array([int(xl), int(yl)])
        finger_coord2 = np.array([int(xr), int(yr)])
        text_results = process.mode_execute(int(mode), image_np, finger_coord1, finger_coord2)

        api_results = []

        if mode == 0 or mode == 1:
            if all(ord(c) < 128 for c in text_results):
                api_results.append(Youdao_EtoZ(text_results))
            else:
                api_results.append(Youdao_ZtoE(text_results))
                api_results.append(Baidu(text_results))
        elif mode == 2:
            api_results.append(Sentence(text_results))
        elif mode == 3:
            api_results.append(Youdao_ZtoE(text_results))
            api_results.append(Baidu(text_results))

        # 存数据库
        if text_results != "无":
            query = Query()
            query.open_id = userid
            query.mode = str(mode)
            query.content = text_results
            query.time = strTime
            result_text = get_result_text(mode, api_results)
            query.result = result_text
            query.save()

    except Exception as err:
        json_data = {'error': str(err)}
        with open("log.txt", 'w') as fw:
            fw.write(str(json_data))
    else:
        json_data = {'text_results': text_results, 'api_results': api_results}
    # finger_coord1 = np.array([xl, yl])
    # finger_coord2 = np.array([xr, yr])
    # json_data = {'text_results': "", 'xl':xl, 'yl':yl, 'xr':xr, 'yr':yr}

    # return HttpResponse(json.dumps(json_data, ensure_ascii=False))
    return JsonResponse(json_data)
