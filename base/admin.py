from django.contrib import admin

from .models import User, Profile, BloodGroup

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(BloodGroup)


# Register your models here.
