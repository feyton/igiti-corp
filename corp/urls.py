from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from index.views import home, species
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from user.views import logout_view, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('species/', species),
    path('user/', include('user.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    path('forestry/', include(('forestry.urls', 'forestry'), namespace='forestry')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
