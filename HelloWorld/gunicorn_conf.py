# -*- ecoding: utf-8 -*-
# @ModuleName: gunicorn_conf.py
# @Function: 
# @Author: qy
# @Time: 2022/2/23 18:25
# gunicorn/django  服务监听地址、端�?
bind = '127.0.0.1:8000'

# gunicorn worker 进程个数，建议为�?CPU核心个数 * 2 + 1
workers = 3

# gunicorn worker 类型�?使用异步的event类型IO效率比较�?
worker_class = "gevent"

# 日志文件路径
errorlog = "/home/cjailab/wx/project/pp-reader/gunicorn.log"
accesslog = "/home/cjailab/wx/project/pp-reader/gunicorn.access.log"
loglevel = "info"

import sys, os

cwd = os.getcwd()
sys.path.append(cwd)
