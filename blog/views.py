from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import PostCreateForm
from .models import Post
# Create your views here.


class PostList(View):
    posts = Post.objects.filter(status=True)
    def get(self, request):
        return render(request, 'blog/post.html', {'posts':self.posts})


class PostDetail(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', {'post':post})


class PostCreate(View):
    template_name = 'blog/post_create.html'
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


class PostUpdate(View):
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


class PostDelete(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        messages.success(request, 'Post deleted successfully', 'success')
        return redirect('blog:home')
