# -*- ecoding: utf-8 -*-
# @ModuleName: youdao_sentence
# @Function: 
# @Author: qy
# @Time: 2022/2/24 14:08

# -*- ecoding: utf-8 -*-
# @ModuleName: 有道翻译句子
# @Function:
# @Author: qy
# @Time: 2022/1/25 21:47

# coding:utf-8
import json

import requests
import hashlib
import time
import random

from django.http import JsonResponse

from . import youdao


def sentence(request):
    if request.method == 'POST':
        postBody = request.body
        request_json = json.loads(postBody)
        word = request_json['input_sentence']
        print(word)
        Youdao = youdao.Youdao(word)
        result = Youdao.run()
        if result == "":
            return JsonResponse({'ret': 1, 'msg': 'youduao_sentence查询失败'})
        return JsonResponse({'ret': 0, 'relist': result})
    else:
        return JsonResponse({'ret': 1, 'msg': 'youduao_sentence请求错误'})


def Sentence(input_sentence):
    word = input_sentence
    print(word)
    Youdao = youdao.Youdao(word)
    result = Youdao.run()
    if result == "":
        return {'ret': 1, 'msg': 'youduao_sentence查询失败'}
    return {'ret': 0, 'relist': result}


if __name__ == '__main__':
    word = input('请输入需要翻译的句子:')
    test = youdao.Youdao(word)
    print(test.run())
