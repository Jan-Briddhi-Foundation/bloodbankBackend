from django.contrib import admin

from .models import User, Profile,  Blood_Request, Donation_Criteria_Form,DonationCriteriaFormField, DonorCriteriaFormSubmission, DonorCriteriaFormFieldData, Donation
from django.contrib.auth.admin import UserAdmin
admin.site.register(Profile)
admin.site.register(Blood_Request)
admin.site.register(DonationCriteriaFormField)
admin.site.register(Donation)
admin.site.register(DonorCriteriaFormFieldData)
admin.site.register(DonorCriteriaFormSubmission)
admin.site.register(Donation_Criteria_Form)


class CustomUserAdmin(UserAdmin):
    add_form = User

    model = User

    list_display = ('name', 'email', 'is_active',
                    'is_staff', 'is_superuser', 'last_login',)
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
