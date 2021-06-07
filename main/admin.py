from django.contrib import admin

from .models import *


class PostImageInline(admin.TabularInline):
    model = PostImages
    max_num = 10
    min_num = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ]


admin.site.register(Category)


