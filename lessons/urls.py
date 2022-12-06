from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings

from .views import handle_page_not_found, handle_bad_request, handle_forbidden, handle_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('register.urls')),

    path('400/', handle_bad_request),
    path('403/', handle_forbidden),
    path('404/', handle_page_not_found),
    path('500/', handle_server_error),

    re_path(r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), serve, {'document_root': settings.STATIC_ROOT}),
]


handler400 = 'lessons.views.handle_bad_request'
handler403 = 'lessons.views.handle_forbidden'
handler404 = 'lessons.views.handle_page_not_found'
handler500 = 'lessons.views.handle_server_error'




