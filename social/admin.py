from django.contrib import admin
from social.models import Post, Comment


# Register your models here.
class CommentAdmin(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "picture",
        "date_posted",
        "date_updated",
        "author"
    )

    inlines = [
        CommentAdmin
    ]


admin.site.register(Post, PostAdmin)