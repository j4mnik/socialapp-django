from django import forms
from social.models import Post, Comment
from accounts.models import User


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={"placeholder": " Title", "class": "title"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Tell others more about that"}))
    picture = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["title", "text", "picture"]


class PostUpdateForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea(attrs={"placeholder": " Title", "class": "title"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Tell others more about that"}))

    class Meta:
        model = Post
        fields = ["title", "text", "picture"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class FollowForm(forms.Form):
    followed_user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

