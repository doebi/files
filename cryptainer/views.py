import os
import random
import Image
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
        'mp4': 'video/mpeg4',
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
                folder = Folder.objects.get(name='temp')
                f = File(name=generateHash(8), folder=folder, data=data)
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

def hasPreview(f, folder):
    dt = str(f.data).split('.')[-1]
    filename = os.path.basename(u'tn_' + unicode(f.data)).replace(' ', '_')
    imageTypes = ['jpg', 'jpeg', 'bmp', 'png']
    if dt in imageTypes:
        src = '/var/files/' + folder + '/'
        thumbnail = 'tn_' + filename.replace(' ', '_')
        try:
            with open(src + thumbnail):
                pass
        except IOError:
            img = Image.open(src + filename)
            img.thumbnail((380, 380))
            img.save('/var/files/' + folder + '/' + thumbnail)
        return True
    else:
        return False

def thumbnail(request, folder, name):
    try:
        folder = Folder.objects.get(name=folder)
    except Folder.DoesNotExist:
        raise Http404
    if request.user.is_authenticated() or folder.is_public:
        try:
            f = File.objects.get(folder=folder, name=name)
        except File.DoesNotExist:
            raise Http404
        filename = os.path.basename(unicode(f.data)).replace(' ', '_')
        temp = filename.split('.')
        dtype = datatypes.get(temp[-1])
        if dtype is None:
            dtype = 'text/plain'
        with open('/var/files/' + folder.name + '/tn_' + filename) as f:
            thumbnail = f.read()
        response = HttpResponse(thumbnail, content_type=dtype)
        #response['Content-Disposition'] = "attachment; filename=%s" %filename
        return response
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
                #f.hasPreview = hasPreview(f, name)
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
    if request.user.is_authenticated() or folder.is_public or folder.name == 'temp':
        try:
            f = File.objects.get(folder=folder, name=name)
        except File.DoesNotExist:
            raise Http404
        f.dl_count = f.dl_count + 1
        f.save()
        filename = os.path.basename(unicode(f.data)).replace(' ', '_')
        temp = filename.split('.')
        dtype = datatypes.get(temp[-1])
        if dtype is None:
            dtype = 'text/plain'
        response = HttpResponse(f.data, content_type=dtype)
        response['Content-Disposition'] = "attachment; filename=%s" %filename
        return response
    else:
        raise PermissionDenied
