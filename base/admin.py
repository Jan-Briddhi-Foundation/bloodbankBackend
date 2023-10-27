from django.contrib import admin

from .models import User, Profile, BloodGroup, Blood_Request, Donation_Form

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(BloodGroup)
admin.site.register(Blood_Request)
admin.site.register(Donation_Form)
