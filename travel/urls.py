from django.urls import path
from . import views
app_name = 'travel'

urlpatterns = [
    # post views
    path('', views.HomeView.as_view(), name="home"),
    path('package/list/', views.PackageView.as_view(), name="package_list"),
    path('package/filter/', views.PackageFilterView.as_view(), name="package_filter"),


    path('location/<int:id>', views.LocationView.as_view(), name="location"),
    path('details/<int:id>', views.PackageDetailsView.as_view(), name="details"),
    path('send-email/', views.SendEmailView.as_view(), name="send_email"),
    path('contact', views.ContactsView.as_view(), name="contact"),
    path('gallery', views.GalleryView.as_view(), name="gallery"),



    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),

]
