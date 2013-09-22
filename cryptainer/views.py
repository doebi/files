from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.core.exceptions import PermissionDenied
from cryptainer.models import Folder, File

def index(request):
    if request.user.is_authenticated():
        folders = Folder.objects.filter(author=request.user)
        return render_to_response('index.html', {'user': request.user, 'folders': folders})
    else:
        raise PermissionDenied


def folder(request, name):
    if request.user.is_authenticated():
        try:
            folder = Folder.objects.get(name=name)
        except Folder.DoesNotExist:
            raise Http404
        files = File.objects.filter(folder=folder)
        if len(files) == 1:
            return get(request, name, 0)
        else:
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
        except Folder.DoesNotExist:
            raise Http404
        response = HttpResponse(f.data)
        response['Content-Disposition'] = "attachment; filename=%s" % unicode(f.data)
        return response
    else:
        raise PermissionDenied
