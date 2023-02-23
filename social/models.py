from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=32)
    text = models.TextField(max_length=255)
    picture = models.ImageField(upload_to="static/post_pictures/", null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField("accounts.User", related_name='liked_posts', blank=True)

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author} - {self.post.title}"
