import os
import random
from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.core.exceptions import PermissionDenied
from cryptainer.models import Folder, File

datatypes = {
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'js': 'application/x-javascript',
        'json': 'application/json',
        'jar': 'application/java-archive',
        'aac': 'audio/aac',
        'ai': 'application/postscript',
        'avi': 'video/avi',
        'bin': 'application/x-binary',
        'bmp': 'image/bmp',
        'bz': 'application/x-bzip',
        'bz2': 'application/x-bzip2',
        }

def generateHash(n):
    word = ''
    for i in range(n):
        word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
    return word


def index(request):
    if request.user.is_authenticated():
        folders = Folder.objects.filter(author=request.user)
        return render_to_response('index.html', {'user': request.user, 'folders': folders})
    else:
        raise PermissionDenied


def upload(request):
    if request.method == 'POST':
        params = request.POST
        user = authenticate(username=params['username'], password=params['password'])
        if user is not None:
            if user.is_active:
                data = request.FILES['file']
                folder = Folder(author=user, name=generateHash(8), is_public=True)
                folder.save()
                f = File(name=generateHash(4), folder=folder, data=data)
                f.save()
                resp = 'Successfully uploaded %s to http://files.doebi.at/%s/%s.' %(data.name, folder.name, f.name)
            else:
                resp = 'user disabled'
        else:
            resp = 'wrong user/password'
        return HttpResponse(resp)
    else:
        #return render_to_response('upload.html', {'form': form})
        return HttpResponse('not yet implemented')


def token(request):
    c = {}
    c.update(csrf(request))
    return HttpResponse(c['csrf_token'])


def folder(request, name):
    try:
        folder = Folder.objects.get(name=name)
    except Folder.DoesNotExist:
        raise Http404
    if request.user.is_authenticated() or folder.is_public:
        try:
            folder = Folder.objects.get(name=name)
        except Folder.DoesNotExist:
            raise Http404
        files = File.objects.filter(folder=folder)
        if len(files) == 1:
            return get(request, name, files[0].name)
        else:
            for f in files:
                f.data = os.path.basename(unicode(f.data))
            data = {
                    'user': request.user,
                    'title': folder.title,
                    'files': files,
                    'folder': name
                    }
            return render_to_response('folder.html', data)
    else:
        raise PermissionDenied


def get(request, folder, name):
    try:
        folder = Folder.objects.get(name=folder)
    except Folder.DoesNotExist:
        raise Http404
    if request.user.is_authenticated() or folder.is_public:
        try:
            f = File.objects.get(folder=folder, name=name)
        except File.DoesNotExist:
            raise Http404
        filename = os.path.basename(unicode(f.data))
        temp = filename.split('.')
        dtype = datatypes.get(temp[-1])
        if dtype is None:
            dtype = 'text/plain'
        response = HttpResponse(f.data, content_type=dtype)
        response['Content-Disposition'] = "attachment; filename=%s" %filename
        return response
    else:
        raise PermissionDenied
