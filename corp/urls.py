from django.contrib import admin
from django.urls import path, include
from index.views import home, species
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from user.views import Dashboard

urlpatterns = [
    path('123FEYTON/', admin.site.urls),
    path('', include('index.urls')),
    path('species/', species),
    path('user/', include('user.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('forestry/', include(('forestry.urls', 'forestry'), namespace='forestry')),
    path('accounts/', include('allauth.urls')),
    path('store/', include(('store.urls', 'store'), namespace='store')),
    path('dashboard/', Dashboard.as_view(), name='profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
