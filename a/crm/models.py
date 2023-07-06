from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    file = models.ImageField(upload_to='images')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='task_images')

class Task(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE, default=1)
    assign = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start = models.DateTimeField(auto_now_add=True)
    estimate_start = models.IntegerField(blank=True, null=True)
    estimate_finish = models.IntegerField(blank=True, null=True)
    estimate_team = models.IntegerField(blank=True, null=True)
    estimate_count = models.IntegerField(blank=True, null=True)
    images = models.ManyToManyField(Image, related_name='tasks')
    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Поле user с связью ForeignKey
    def __str__(self):
        return self.content

class Status(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['order']

class File(models.Model):
    file = models.FileField()

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.DecimalField(max_digits=10, decimal_places=2)