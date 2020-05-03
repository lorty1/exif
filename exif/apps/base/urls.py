from django.conf.urls import url
from django.views.generic import TemplateView
from base import views

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='home'),
]