# -*- ecoding: utf-8 -*-
# @ModuleName: upload
# @Function: 
# @Author: qy
# @Time: 2022/2/24 15:57


'''服务器'''
import os

from django.http import HttpResponse

'''获取POST到服务器的文件对象'''


def img(request):
    if request.method == "POST":
        files = request.FILES
        '''
		 需要通过小程序端的key（image）获取二进制数据
		 获取文件内容
		'''
        content = files.get('example', None).read()
        # print(content)
        '''
        设置保存路径
            settings.IMAGES_DIR 已经默认设定
            默认保存文件名字为aaa.jpg
        '''
        path = os.path.join(r"C:\Users\11343\Desktop\挑战杯\django\wx\api", 'example.mp3')
        print(path)
        with open(path, 'wb') as f:
            f.write(content)
        return HttpResponse("success")
    else:
        return HttpResponse("failed")


from django.shortcuts import render
from django.http import HttpResponse


def upload_file(request):
    # 请求方法为POST时,进行处理;
    if request.method == "POST":
        # 获取上传的文件,如果没有文件,则默认为None;
        File = request.FILES.get("myfile", None)
        if File is None:
            return HttpResponse("no files for upload!")
        else:
            # 打开特定的文件进行二进制的写操作;
            with open("/tmp/%s" % File.name, 'wb+') as f:
                # 分块写入文件;
                for chunk in File.chunks():
                    f.write(chunk)
            return HttpResponse("upload over!")
    else:
        return render(request, 'polls/upload.html')
