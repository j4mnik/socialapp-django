from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from social.views import FeedView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, post_like, \
    post_unlike, ProfileView, FindFriendsView, follow_user, unfollow_user, FollowedUsersListView, FollowersListView

urlpatterns = [
    path("", FeedView.as_view(), name="home"),
    path("post/new/", PostCreateView.as_view(), name="post_new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/like/', post_like, name='post_like'),
    path('post/<int:pk>/unlike/', post_unlike, name='post_unlike'),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path('user/<int:user_id>/followers/', FollowersListView.as_view(), name='followers'),
    path('user/<int:user_id>/followed_users/', FollowedUsersListView.as_view(), name='followed_users'),
    path('find-friends/', FindFriendsView.as_view(), name='find_friends'),
    path('follow/<int:user_id>/', follow_user, name='follow'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
