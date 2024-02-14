from django.contrib import admin
from .models import *

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_avail', 'short_description', 'full_description', 'image')
    prepopulated_fields = {'slug': ('name', 'price')}

admin.site.register(Good)

