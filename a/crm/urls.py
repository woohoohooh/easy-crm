from django.urls import path
from .views import index, create_task, task_detail, edit_task, save_image

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('create/', create_task, name='create_task'),
    path('task/<int:task_id>/', task_detail, name='task_detail'),
    path('task/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('save_image/', save_image, name='save_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
