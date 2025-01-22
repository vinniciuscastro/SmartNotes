from django.contrib import admin
from . import models
from .models import Note
# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('pk','title', 'likes')
    list_display_links = ('title',)
    
    
admin.site.register(Note, NoteAdmin)  