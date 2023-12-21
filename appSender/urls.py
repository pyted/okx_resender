from django.urls import path, re_path
from appSender import views

app_name = 'appSender'
urlpatterns = [
    path('', views.index_handler, name='index'),
    re_path('^(?P<path>.+)$', views.api_handler, name='api'),
]
