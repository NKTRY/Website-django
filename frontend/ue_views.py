import json
import os
import time
import uuid

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from nktc import settings
from config import config


def customConfig(request):
    params = request.GET
    if params['action'] == 'uploadimage':
        return ueditor_ImgUp(request)
    return HttpResponse(json.dumps(config))


def __myuploadfile(fileObj, source_pictitle, source_filename, fileorpic='pic'):
    """ 一个公用的上传文件的处理 """
    myresponse = ""
    if fileObj:
        filename = fileObj.name
        fileExt = filename.split('.')[1]
        file_name = str(uuid.uuid1())
        subfolder = time.strftime("%Y%m")
        if not os.path.exists(settings.SRC_ROOT[1] + subfolder):
            os.makedirs(settings.SRC_ROOT[1] + subfolder)
        path = str(subfolder + '/' + file_name + '.' + fileExt)

        if fileExt.lower() in (
                'jpg', 'jpeg', 'bmp', 'gif', 'png', "rar", "doc", "docx", "zip", "pdf", "txt", "swf", "wmv"):

            phisypath = settings.SRC_ROOT[1] + path
            destination = open(phisypath, 'wb+')
            for chunk in fileObj.chunks():
                destination.write(chunk)
            destination.close()


            real_url = '/static/img/' + subfolder + '/' + file_name + '.' + fileExt
            myresponse = "{'original':'%s','url':'%s','title':'%s','state':'%s'}" % (
                source_filename, real_url, source_pictitle, 'SUCCESS')
    return myresponse


@csrf_exempt
def ueditor_ImgUp(request):
    """ 上传图片 """
    fileObj = request.FILES.get('upfile', None)
    source_pictitle = request.POST.get('pictitle', '')
    source_filename = request.POST.get('fileName', '')
    response = HttpResponse()
    myresponse = __myuploadfile(fileObj, source_pictitle, source_filename, 'pic')
    response.write(myresponse)
    return response