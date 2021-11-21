from django import forms
from django.forms import fields
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'body', 'snippet', 'image', 'status']