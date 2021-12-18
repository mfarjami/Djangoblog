from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.tasks import all_bucket_objects_task

class BucketHome(LoginRequiredMixin, View):
    template_name = 'blog/bucket.html'
    def get(self, request):
        objects = all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})