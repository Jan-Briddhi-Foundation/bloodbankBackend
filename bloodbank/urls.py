from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('base/', include('base.urls')),
    path('api/auth/', include('djoser.urls')),

    # path('api/login/', include('rest_social_auth.urls_token')),
    # path('api/login/', include('rest_social_auth.urls_knox')),

    path('api/', include('base.api.urls')),
    path('social_auth/', include('base.social_auth.urls')),
    # path('accounts/', include('allauth.urls')),
    path('auth-token/', include('djoser.urls.authtoken')),

    # path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls'))

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
