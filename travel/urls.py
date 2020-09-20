from django.urls import path
from . import views
app_name = 'travel'

urlpatterns = [
# post views
path('', views.HomeView.as_view(), name="home"),
path('contact', views.contact, name="contact"),
]