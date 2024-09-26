# blog/context_processors.py

from django.db.models import Count
from .models import Post, PostCategory

def categories_with_post_count(request):
    categories = PostCategory.objects.all().annotate(post_count=Count('posts'))
    latest_posts = Post.objects.order_by('-date_posted')[:5]  # Get the latest 5 posts
    return {
        'categories_with_post_count': categories,
        'latest_posts': latest_posts  # Add the latest posts to the context
    }

def categories(request):
    return {'categories': PostCategory.objects.all()}