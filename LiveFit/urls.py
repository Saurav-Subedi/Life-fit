from django.contrib import admin
from django.urls import path, include
admin.site.site_header="LIveFit"
admin.site.site_title ="fitness Equipment store"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), 
]
