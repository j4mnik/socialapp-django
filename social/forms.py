from django import forms
from social.models import Post, Comment


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={"placeholder": " Title", "class": "title"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Tell others more about that"}))

    class Meta:
        model = Post
        fields = ["title", "text", "picture"]

        def form_valid(self, form):
            form.instance = self.request.user
            return super().form_valid(form)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
