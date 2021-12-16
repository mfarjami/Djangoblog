from django import forms
from django.forms import fields
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'body', 'snippet', 'image', 'status']


class ContactUsForm(forms.Form):
    name = fields.CharField(max_length=100, required=True)
    subject = forms.CharField(max_length=30, required=True)
    email = fields.EmailField(required=True)
    phone = fields.CharField(max_length=11, required=False)
    message = fields.CharField(widget=forms.Textarea, required=True)


class SharePostForm(forms.Form):
    name = fields.CharField(max_length=100, required=True)
    to = fields.EmailField(required=True)
    message = fields.CharField(widget=forms.Textarea, required=True)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

