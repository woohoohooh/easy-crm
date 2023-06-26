from django.urls import path
from .views import index_list, create_task, edit_task, delete_image

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_list, name='index_list'),
    path('create/', create_task, name='create_task'),
    path('task/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('image/<int:image_id>/delete/', delete_image, name='delete_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
