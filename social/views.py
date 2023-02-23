from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.edit import View, UpdateView, DeleteView, FormMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from social.forms import PostCreateForm, CommentForm
from social.models import Post


# Create your views here.
class FeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "social/home.html"

    def get_queryset(self):
        return Post.objects.order_by('-date_posted')


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'social/post_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.liked_by.add(request.user)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=self.get_object().pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))


def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    post.liked_by.add(request.user)
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
            redirect_url = reverse('post_detail', kwargs={'pk': post.pk})
            return redirect(redirect_url)
        return render(request, self.template_name, {'form': form})


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'picture']
    template_name = 'social/post_edit.html'
    success_url = reverse_lazy('')

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "social/post_delete.html"
    success_url = reverse_lazy("home")
