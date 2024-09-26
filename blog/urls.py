from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('category/<slug:slug>/', views.category_detail, name='category-detail'),
    path('search/', views.search, name='search'),  # Add this line for search
]