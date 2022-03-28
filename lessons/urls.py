from django.contrib import admin
from django.urls import path, include

from .views import handle_page_not_found, handle_bad_request, handle_forbidden, handle_server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('register.urls')),

    path('400/', handle_bad_request),
    path('403/', handle_forbidden),
    path('404/', handle_page_not_found),
    path('500/', handle_server_error),
]


handler400 = 'lessons.views.handle_bad_request'
handler403 = 'lessons.views.handle_forbidden'
handler404 = 'lessons.views.handle_page_not_found'
handler500 = 'lessons.views.handle_server_error'




