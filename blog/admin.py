from django.contrib import admin
from .models import Post,Profile,Comment,PostCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'category_name')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(PostCategory)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)