# Generated by Django 4.2.2 on 2023-06-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_remove_task_image_task_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='files',
        ),
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/'),
        ),
    ]