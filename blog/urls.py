from django.urls import path
from . import views
app_name = "blog"

urlpatterns = [
    path('', views.BlogHomeView.as_view(), name="blog_home"),
    path('<str:category_name>/<int:category_id>',
         views.CategoryPostView.as_view(), name="category_post"),
    path('single/post/<int:pk>',
         views.SignlePostView.as_view(), name="single_post"),

    path('search/post',
         views.SearchPostView.as_view(), name="search_post"),
]
