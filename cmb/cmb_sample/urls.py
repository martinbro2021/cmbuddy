# For more information please see https://docs.djangoproject.com/en/4.1/topics/http/urls/

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("cmb_home.urls")),
    path('contact/', include("cmb_contact.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
