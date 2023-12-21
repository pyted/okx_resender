import traceback
from appSite.models import SenderLogModel
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.parse as up
import requests.api
import appSite.globalvar as gv


def index_handler(request):
    return render(request, 'index.html', {})


def resender(request, path, api_url):
    # 需要保留的header key
    header_keys = [
        'Content-Type',
        'OK-ACCESS-KEY',
        'OK-ACCESS-SIGN',
        'OK-ACCESS-TIMESTAMP',
        'OK-ACCESS-PASSPHRASE',
        'x-simulated-trading',
    ]
    # request中得到的header key转小写
    request_header_lower_map = {}
    for k, v in request.headers.items():
        request_header_lower_map[k.lower()] = v
    # 构造headers
    headers = {}
    for key in header_keys:
        if key.lower() in request_header_lower_map.keys():
            headers[key] = request_header_lower_map[key.lower()]
    method = request.method.lower()
    if method == 'get':
        params = request.GET.dict()
        params.pop('url', None)
        params_no_empty = {}
        for k, v in params.items():
            if v != '':
                params_no_empty[k] = v
        if params_no_empty:
            path = path + '?' + up.urlencode(params_no_empty)
    url = up.urljoin(api_url, path)
    body = request.body
    response = requests.api.request(
        method=method,
        url=url,
        headers=headers,
        data=body,
    )
    text = response.text
    return text


def base_api_handler(request, path, api_url):
    # ip
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META.get('HTTP_X_FORWARDED_FOR')
    else:
        ip = request.META.get('REMOTE_ADDR')
    if not ip in gv.get('allowed_ips'):
        error_msg = 'Forbidden IP:' + ip
        status = 403
        if gv.get('use_log'):
            if not ip:
                ip = 'UnKnow'
            SenderLogModel(
                ip=ip,
                status=0,
                error_msg='Forbidden IP ' + ip
            ).save()
        error_data = {'code': '-1', 'data': {}, 'msg': error_msg}
        return JsonResponse(error_data, status=status)
    # resender
    try:
        text = resender(request, path, api_url)
        status = 200
        if gv.get('use_log'):
            SenderLogModel(
                ip=ip,
                status=1,
                error_msg='',
            ).save()
        return HttpResponse(str(text), status=status)
    except:
        error_msg = 'Error Okx Resender ' + traceback.format_exc()
        error_data = {'code': '-2', 'data': {}, 'msg': error_msg}
        status = 500
        if gv.get('use_log'):
            SenderLogModel(
                ip=ip,
                status=0,
                error_msg=error_msg,
            ).save()
        return JsonResponse(error_data, status=status)


@csrf_exempt
def api_handler(request, path):
    return base_api_handler(request, path, 'https://www.okex.com')
