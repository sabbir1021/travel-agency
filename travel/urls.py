from django.urls import path
from . import views
app_name = 'travel'

urlpatterns = [
# post views
path('', views.home, name="home"),
path('contact', views.contact, name="contact"),
]