from django.db import models
from accounts.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    # body = models.TextField()
    body = RichTextField()
    snippet = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images/')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.snippet = slugify(self.title)
        super().save(*args, **kwargs)