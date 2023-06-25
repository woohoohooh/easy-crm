from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    assign = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    estimate_start = models.IntegerField()
    estimate_finish = models.IntegerField()
    estimate_team = models.IntegerField()
    images = models.ManyToManyField('Image', related_name='tasks')
    files = models.ManyToManyField('File')
    comments = models.ManyToManyField('Comment')

class Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()

class File(models.Model):
    file = models.FileField(upload_to='task_files/')

class Image(models.Model):
    task = models.ForeignKey(Task, related_name='task_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')