from django.contrib import admin
from blog_api.models import Post


class PostAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')

admin.site.register(Post, PostAdmin)