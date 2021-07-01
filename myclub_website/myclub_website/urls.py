from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),
]

#  customization

admin.site.site_header = "My Club Administration Page"
admin.site.site_title = "My Club"
admin.site.index_title = "Welcome to Admin area 🚀"

#  DONE
