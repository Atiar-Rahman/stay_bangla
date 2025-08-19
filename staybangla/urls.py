
from django.contrib import admin
from django.urls import path,include, re_path
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')), 
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('api/v1/',include('api.urls'),name='api-root'),
]+ debug_toolbar_urls()
