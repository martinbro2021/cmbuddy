# For more information please see https://docs.djangoproject.com/en/4.1/topics/http/urls/

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from cmb_sample.settings import DEBUG, MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("cmb_home.urls")),
    path('contact/', include("cmb_contact.urls"))
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
