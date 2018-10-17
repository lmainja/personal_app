#posts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from tinymce import HTMLField

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField('Content', null=True) 
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def get_absolute_url(self):
        return reverse('posts:post-detail', kwargs={'pk': self.pk})

    def summary(self):
        return self.content[:50]

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name=models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    headline = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='authors')

    def __str__(self):
        return last_name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    creator = models.CharField(max_length=200)
    text = models.TextField(max_length=4000)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
    
