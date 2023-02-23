from django.urls import path
from social.views import FeedView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, post_like

urlpatterns = [
    path("post/new/", PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/like/', post_like, name='post_like'),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("", FeedView.as_view(), name="home"),
]
