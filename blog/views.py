from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, PostCategory
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Count

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # Call the base implementation to get the existing context
        context = super().get_context_data(**kwargs)
        
        # Add latest 5 posts to the context
        context['latest_posts'] = Post.objects.order_by('-date_posted')[:5]
        context['categories_with_post_count'] = PostCategory.objects.all().annotate(post_count=Count('posts'))
        context['categories'] = PostCategory.objects.all()
        return context


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Post.objects.filter(title__icontains=query)  # You can add more fields to search within.

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'blog/search_results.html', context)


def category_detail(request, slug):
    category = get_object_or_404(PostCategory, slug=slug)
    posts = Post.objects.filter(category_name=category)

    # Pagination logic
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': page_obj,  # Use page_obj instead of posts
    }
    return render(request, 'blog/category_detail.html', context)


# Single post detail view
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent=None)
    new_comment = None
    total_comments = post.comments.count()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            parent_id = request.POST.get('parent_id')
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)
            new_comment.save()
            return redirect('post-detail', slug=post.slug)  # Redirect to the post detail page
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment,
        'total_comments': total_comments,
    }
    return render(request, 'blog/post_detail.html', context)