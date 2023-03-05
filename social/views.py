from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import View, UpdateView, DeleteView, FormMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from social.forms import PostCreateForm, CommentForm, FollowForm, PostUpdateForm
from social.models import Post, Follower
from accounts.models import User


# Create your views here.
class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "social/home.html"

    def get_queryset(self):
        user_following = self.request.user.following.values_list('followed_user', flat=True)
        queryset = Post.objects.filter(author_id__in=user_following)
        queryset = queryset.order_by('-date_posted')
        return queryset


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'social/post_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        post = self.get_object()
        user = self.request.user
        context['liked'] = post.liked_by.filter(id=user.id).exists()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        post.liked_by.add(user)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))


@login_required
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    post.liked_by.add(request.user)
    return redirect('post_detail', pk=post.pk)


@login_required
def post_unlike(request, pk):
    post = Post.objects.get(pk=pk)
    post.liked_by.remove(request.user)
    return redirect('post_detail', pk=post.pk)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm
    template_name = 'social/post_new.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            redirect_url = reverse('post_detail', kwargs={'pk': post.pk})
            return redirect(redirect_url)
        return render(request, self.template_name, {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        picture = form.cleaned_data.get('picture')
        if picture:
            form.instance.picture = picture
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "social/post_delete.html"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "social/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(author=user)
        context['followers'] = user.followers.all()
        context['following'] = user.following.all()

        if self.request.user.is_authenticated:
            is_following = user.followers.filter(follower_user=self.request.user).exists()
            context['is_following'] = is_following

        return context


class FindFriendsView(LoginRequiredMixin, FormMixin, ListView):
    model = User
    template_name = "social/find_friends.html"
    form_class = FollowForm
    success_url = reverse_lazy('find_friends')

    def get_queryset(self):
        queryset = super().get_queryset().exclude(pk=self.request.user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        following = user.following.all().values_list('followed_user_id', flat=True)
        context['following'] = following
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            followed_user = form.cleaned_data['followed_user']
            Follower.objects.create(follower_user=request.user, followed_user=followed_user)
        return super().form_valid(form)


class FollowersListView(ListView):
    model = Follower
    template_name = 'social/follower_users.html'
    context_object_name = 'followers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        context['user'] = user
        return context

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return Follower.objects.filter(followed_user=user)


class FollowedUsersListView(ListView):
    model = Follower
    template_name = 'social/followed_users.html'
    context_object_name = 'followed_users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        context['user'] = user
        return context

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return Follower.objects.filter(follower_user=user)


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    follower = request.user
    Follower.objects.create(follower_user=follower, followed_user=user_to_follow)
    return redirect('profile', pk=user_id)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follower = request.user
    Follower.objects.filter(follower_user=follower, followed_user=user_to_unfollow).delete()
    return redirect('profile', pk=user_id)
