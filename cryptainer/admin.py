from django.contrib import admin
from cryptainer.models import Folder, File

class FilesInline(admin.StackedInline):
    model = File

class FolderAdmin(admin.ModelAdmin):
    inlines = [FilesInline]

admin.site.register(Folder, FolderAdmin)
admin.site.register(File)
