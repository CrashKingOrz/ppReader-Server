# -*- ecoding: utf-8 -*-
# @ModuleName: pinyin
# @Function: 
# @Author: qy
# @Time: 2022/3/8 20:47
import json
import re
import requests
from django.http import HttpResponse, JsonResponse
from lxml import etree
from pypinyin import pinyin, lazy_pinyin


def pinyin_py(request):
    if request.method == 'POST':
        postBody = request.body
        request_json = json.loads(postBody)
        word = request_json['input_word']  # 返回网页源代码
        result = pinyin(word)  # 英汉
        return JsonResponse({'ret': 0, 'relist': result})
    else:
        return JsonResponse({'ret': 1, 'msg': 'pinyin请求错误'})


if __name__ == '__main__':
    print(pinyin('聪明的小兔子'))
