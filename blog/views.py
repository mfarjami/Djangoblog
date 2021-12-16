from django import forms
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import PostCreateForm, ContactUsForm, SharePostForm, AddCommentForm 
from django.core.mail import send_mail
from .mixins import AuthorAccessMixin
from .models import Comment, Post
# Create your views here.


class PostList(View):
    posts = Post.objects.filter(status=True)
    def get(self, request):
        return render(request, 'blog/post.html', {'posts':self.posts})


class PostDetail(View):
    form_class = AddCommentForm
    template_name = 'blog/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Comments = Comment.objects.filter(post=post, active=True, is_reply=False)
        reply_form = self.form_class()
        context={
            'post':post,
            'comments':Comments, 
            'form':self.form_class,
            'reply':reply_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Comment sent successfully', 'success')
            return redirect('blog:post_detail', pk)
        else:
            context={
            'post':post,
            'form':form,
            }
            return render(request, self.template_name, context)


class PostCreate(View):
    template_name = 'blog/post_create.html' # Replace with your template
    form_class = PostCreateForm

    def get(self, request):
        return render(request, self.template_name, {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post created successfully', 'success')
            return redirect('blog:home')
        return render(request, self.template_name, {'form':form})


class PostUpdate(AuthorAccessMixin, View):
    template_name = 'blog/post_update.html'
    form_class = PostCreateForm

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form':form,})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = self.form_class(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully', 'success')
            return redirect('blog:post_detail', post_id)
        return render(request, self.template_name, {'form':form})


class PostDelete(AuthorAccessMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, 'Post deleted successfully', 'success')
        return redirect('blog:home') 


class ContactUs(View):
    form_class = ContactUsForm
    template_name = 'blog/contact_us.html'

    def get(self, request):
        return render(request, self.template_name, {'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = cd['subject']
            message = cd['message']
            name = cd['name']
            email = cd['email']
            phone = cd['phone']
            msg = f'Subject: {subject}\n\n{message}\n\nName: {name}\nEmail: {email}\nPhone: {phone}'
            send_mail(subject, msg, 'biroghlan95@gmail.com', ['biroghlan95@gmail.com'], fail_silently=True)
            messages.success(request, 'Email sent successfully', 'success')
            return redirect('blog:home')
        else:
            messages.error(request, 'Email not sent', 'error')
            return render(request, self.template_name, {'form':form})


class SharePostView(View):
    form_class = SharePostForm
    template_name = 'blog/share_post.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, status=True, id=post_id)
        return render(request, self.template_name, {'form':self.form_class, 'post':post})

    def post(self, request, post_id):
        post = get_object_or_404(Post, status=True, id=post_id)
        form = SharePostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            name = cd['name']
            subject = f'{name} has invited you to read {post.title}'
            message = cd['message']
            to = cd['to']
            msg = f'{name} has invited you to read the {post.title} post at the following address.\n {message} \n {post_url}'
            send_mail(subject, msg, 'biroghlan95@gmail.com', [to], fail_silently=True)
            messages.success(request, f'Post {post.title} for {to} shared successfully', 'success')
            return redirect('blog:home')
        else:
            messages.error(request, '{post.title} post was not sent to {to}', 'error')
            return render(request, self.template_name, {'form':form, 'post':post})
            

class AddReplyView(View):
    def post(self, request, comment_id, post_id):
        comment = get_object_or_404(Comment, id=comment_id)
        post = get_object_or_404(Post, id=post_id)
        form = AddCommentForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.reply = comment
            new_reply.post = post
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request, 'Your reply sent successfully', 'success')
            return redirect('blog:post_detail', post_id)
        else:
            messages.error(request, 'Your reply not sent', 'error')
            return redirect('blog:post_detail', post_id)
            