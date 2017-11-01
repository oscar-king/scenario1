from django.contrib import admin

from .models import Post #, Category

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ["name", "slug"]
#     prepopulated_fields = {'slug': ('name',)}
#
# admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "lastUpdated", "timestamp"]
    list_filter = ["lastUpdated", "timestamp"]
    search_fields = ["title", "content"]
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
