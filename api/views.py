# django视图
from django.http import HttpResponse, JsonResponse
from .models import User
from .models import Query
from .models import Time
import json
import time


def get_msg(request):
    if request.method == 'POST':
        print("the POST method")
        concat = request.POST
        postBody = request.body
        print(concat)
        # print(type(postBody))
        print(postBody)
        json_result = json.loads(postBody)
        print(json_result)
        return HttpResponse("Hello world")
    else:
        return HttpResponse("Hello world")


def InsertUser(request):
    user = User()
    user.email = request.GET.get('email')
    user.name = request.GET.get('name')
    user.password = request.GET.get('password')
    res = User.objects.filter(email=user.email)
    if len(res) > 0:
        json_data = {'status': 500, 'msg': '注册邮箱已经存在！'}
    else:
        user.save()
        json_data = {'status': 200, 'id': user.id, 'type': 'user'}
    return JsonResponse(json_data)


def Login(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    res = User.objects.filter(email=email)
    if len(res) != 1:
        json_data = {'status': 500, 'msg': '登陆失败！用户名或密码错误'}
    elif res[0].password == password:
        json_data = {'status': 200, 'id': res[0].id, 'name': res[0].name, 'msg': '登陆成功！'}
    else:
        json_data = {'status': 500, 'msg': '登陆失败！用户名或密码错误'}
    return JsonResponse(json_data)


def InsertTime(request):
    time = Time()
    time.open_id = request.GET.get('open_id')
    time.start_time = request.GET.get('start_time')
    time.end_time = request.GET.get('end_time')
    time.duration = request.GET.get('duration')
    time.save()
    json_data = {'status': 200, 'id': time.id, 'type': 'time'}
    return JsonResponse(json_data)


def getAllUserInfo(request):
    # open_id = request.GET.get('open_id')

    results = User.objects.filter()
    arr = []
    for res in results:
        content = {'id': res.id, 'name': res.name, 'email': res.email, 'password': res.password}
        arr.append(content)
    json_data = {'status': 200, 'res': arr}
    # return HttpResponse('NB')
    return JsonResponse(json_data)


def getAllQueryInfo(request):
    results = Query.objects.filter()
    arr = []
    for res in results:
        content = {'id': res.id, 'open_id': res.open_id, 'content': res.content, 'mode': res.mode, 'time': res.time,
                   'result': res.result}
        arr.append(content)
    json_data = {'status': 200, 'res': arr}
    # return HttpResponse('NB')
    return JsonResponse(json_data)


def getQueryInfo(request):
    open_id = request.GET.get('usrid')
    results = Query.objects.filter(open_id=open_id)
    arr = []
    for res in results:
        content = {'id': res.id, 'open_id': res.open_id, 'content': res.content, 'mode': res.mode, 'time': res.time,
                   'result': res.result}
        arr.append(content)
    json_data = {'status': 200, 'res': arr}
    # return HttpResponse('NB')
    return JsonResponse(json_data)


def getQueryCounts(request):
    try:
        open_id = request.GET.get('usrid')
        datedict = {}
        modedict = {}
        allcount = 0
        results = Query.objects.filter(open_id=open_id)
        for res in results:
            date = str(res.time).split(' ')[0]
            mode = str(res.mode)
            if date not in datedict:
                datedict[date] = 0
            datedict[date] += 1
            if mode not in modedict:
                modedict[mode] = 0
            modedict[mode] += 1
            allcount += 1
        timeStamp = time.time()
        localTime = time.localtime(timeStamp)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        today = strTime.split(" ")[0]
        if today not in datedict:
            datedict[today] = 0
        todaytimes = datedict[today]
        json_data = {'status': 200, 'res': datedict, 'modedict': modedict, 'all': allcount, 'days': len(datedict),
                     'today': todaytimes}
    except Exception as err:
        json_data = {'status': 500, 'error': str(err)}
    return JsonResponse(json_data)
