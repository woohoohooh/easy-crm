# Generated by Django 4.2.2 on 2023-06-24 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_file_remove_task_file_task_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='image',
        ),
        migrations.AddField(
            model_name='task',
            name='files',
            field=models.ImageField(blank=True, null=True, upload_to='task_files/'),
        ),
    ]
