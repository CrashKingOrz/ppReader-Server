"""wx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from . import youdao_word
from . import youdao_sentence
from . import upload
from . import download
from . import pinyins

from . import baidu_dict

urlpatterns = [
    path('text_search', views.get_msg),  # 测试
    path('youdao_word/ZtoE', youdao_word.youduao_ZtoE),  # 有道 中文-英文
    path('youdao_word/EtoZ', youdao_word.youduao_EtoZ),  # 有道 英文-中文
    path('youdao_sentence', youdao_sentence.sentence),  # 有道 句子翻译
    path('download', download.download_file),  # ������ȡ
    path('get_word_voice', download.get_word_voice),  # ���ز���
    path('robot', download.robot_api),  # ���ز���
    # path('voice_ass', voice_ass.voice_ass), # 语音助手
    path('baidu', baidu_dict.baidu),  # 百度汉语词典
    path('pinyin', pinyins.pinyin_py),  # �ٶȺ���ʵ�
    path('getalluserinfo', views.getAllUserInfo),
    path('getallqueryinfo', views.getAllQueryInfo),
    path('getqueryinfo', views.getQueryInfo),
    path('getquerycounts', views.getQueryCounts),
    path('insertuser', views.InsertUser),
    path('inserttime', views.InsertTime),
    path('login', views.Login),
]
