from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Task, Status, Image
from .forms import TaskForm
from django.core.files.base import ContentFile
import base64


@transaction.atomic
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()

            # Получаем текущий список URL изображений из базы данных
            image_urls = list(task.images.values_list('image.url', flat=True))

            # Обрабатываем добавленные изображения из запроса
            if 'image' in request.FILES:
                image_files = request.FILES.getlist('image')
                for image_file in image_files:
                    image = Image.objects.create(task=task, image=image_file)
                    image_urls.append(image.image.url)

            # Сохраняем обновленный список URL изображений в сессию
            request.session['image_urls'] = image_urls

            return redirect('edit_task', task_id=task_id)
    else:
        form = TaskForm(instance=task)

    # Получаем список URL изображений из сессии и передаем его в шаблон
    image_urls = request.session.get('image_urls', [])
    return render(request, 'crm/edit_task.html', {'form': form, 'task': task, 'image_urls': image_urls})


@csrf_exempt
def save_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image_file')
        task_id = request.POST.get('task_id')

        task = get_object_or_404(Task, id=task_id)
        image = Image.objects.create(task=task, image=image_file)

        image_url = image.image.url  # Get the URL of the saved image

        return JsonResponse({'success': True, 'image_url': image_url})
    else:
        return JsonResponse({'success': False})


def index(request):
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
            return redirect('index')
    else:
        task_form = TaskForm()
    return render(request, 'crm/edit_task.html', {'task_form': task_form})

def task_detail(request, task_id):
    task = Task.objects.get(pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
    else:
        form = TaskForm(instance=task)
    context = {
        'task': task,
        'form': form,
    }
    return render(request, 'crm/task_detail.html', context)
