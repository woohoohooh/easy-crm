from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Status, Image
from .forms import TaskForm
from django.core.files.base import ContentFile
import base64
import os

def save_image(request, task):
    if 'image' in request.FILES:
        image_file = request.FILES['image']
        image = Image.objects.create(file=image_file, task=task)
        task.images.add(image)
    elif 'image_base64' in request.POST:
        image_base64 = request.POST['image_base64']
        if ';' in image_base64:
            format, imgstr = image_base64.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name='image.' + ext)
            image = Image.objects.create(file=image_file, task=task)
            task.images.add(image)

def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            save_image(request, task)
            form.save()
            return redirect('edit_task', task_id=task_id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'crm/edit_task.html', {'form': form, 'task': task})

def estimates(estimate_finish, estimate_team):
    if estimate_team:
        return estimate_team
    else:
        return estimate_finish

def delete_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    task_id = image.task_id
    image_path = image.file.path  # Получаем путь к файлу изображения
    image.delete()  # Удаляем объект Image
    os.remove(image_path)  # Удаляем файл из файловой системы
    return redirect('edit_task', task_id=task_id)

def index_list(request):
    statuses = Status.objects.all()
    tasks_by_status = {}
    for status in statuses:
        tasks = Task.objects.filter(status=status)
        tasks_by_status[status] = tasks
    context = {'tasks_by_status': tasks_by_status}
    return render(request, 'crm/index.html', context)

def create_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()
            return redirect('index_list')
    else:
        task_form = TaskForm()
    return render(request, 'crm/edit_task.html', {'task_form': task_form})