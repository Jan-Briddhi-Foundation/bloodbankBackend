from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile_type = request.user.profile.profile_type

            if profile_type == 'donor':
                return redirect('donor_home')
            elif profile_type == 'patient':
                return redirect('patient_home')
            else:
                return redirect('user_details')

        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
