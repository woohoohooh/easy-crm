# Generated by Django 4.2.2 on 2023-06-24 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_image_remove_task_image_task_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='images',
        ),
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]