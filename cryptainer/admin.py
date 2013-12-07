from django.contrib import admin
from cryptainer.models import Folder, File

class FilesInline(admin.StackedInline):
    model = File
    readonly_fields = ('dl_count',)

class FolderAdmin(admin.ModelAdmin):
    inlines = [FilesInline]

admin.site.register(Folder, FolderAdmin)
