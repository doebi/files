from django.http import Http404, HttpResponse
import os
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

def index(request):
    if request.user.is_authenticated():
        folders = Folder.objects.filter(author=request.user)
        return render_to_response('index.html', {'user': request.user, 'folders': folders})
    else:
        raise PermissionDenied


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
