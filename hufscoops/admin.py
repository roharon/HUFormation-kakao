from django.contrib import admin
from .models import *

# 출력할 ResourceAdmin 클래스를 만든다
class ResourceAdmin(admin.ModelAdmin):
  pass

# 클래스를 어드민 사이트에 등록한다.
admin.site.register(Log, ResourceAdmin)
admin.site.register(Menu, ResourceAdmin)

# Register your models here.
