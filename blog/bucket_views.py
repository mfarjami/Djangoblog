from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import tasks

class BucketHome(LoginRequiredMixin, View):
    template_name = 'blog/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})

    
class BucketDelete(LoginRequiredMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'Object deleted successfully', 'success')
        return redirect('blog:bucket_home')
    

class BucketDownload(LoginRequiredMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'Object downloaded successfully', 'success')
        return redirect('blog:bucket_home')

