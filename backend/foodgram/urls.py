from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# from food.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('food.urls')),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
