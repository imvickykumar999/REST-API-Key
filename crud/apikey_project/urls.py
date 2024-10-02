# apikey_project/urls.py
from django.contrib import admin
from django.urls import path, include
from apiapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apiapp.urls')),
    path('', views.index, name='index'),
]
