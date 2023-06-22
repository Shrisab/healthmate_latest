from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(doctor)
admin.site.register(consultationform)
admin.site.register(Profile)
admin.site.register(Post)
# admin.site.register(Comment)
