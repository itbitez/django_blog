from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    user_info = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'

    # Optional: Resize the uploaded image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

class PostCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class Post(models.Model):
    image = models.ImageField(upload_to='blog')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category_name = models.ForeignKey(PostCategory, related_name='posts', on_delete=models.CASCADE)
    content = RichTextField()
    excerpt = models.TextField()
    date_posted = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not already set
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # Link to the Post model
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)  # Store the date and time of the comment
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)  # For replies

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

