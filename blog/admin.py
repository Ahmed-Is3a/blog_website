from django.contrib import admin

from blog.models import Comment, Post

# Register your models here.

admin.site.register(Post)
# admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post']
    list_filter = ['active']
    search_fields = ['name']
    

