from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Blog)

admin.site.register(BlogCategory)

admin.site.register(Comment)

admin.site.register(Reply)

admin.site.register(Bookmark)