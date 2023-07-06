from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Status, Image, Bid
from .forms import TaskForm
from django.core.files.base import ContentFile
import base64
import os
from decimal import Decimal
from .models import Comment

def create_comment(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id)
        content = request.POST.get('content')
        user_id = request.POST.get('user')  # Получение значения user_id из request.POST
        Comment.objects.create(task=task, content=content, user_id=user_id)  # Сохранение значения user_id
        return redirect('edit_task', task_id=task_id)
    else:
        return HttpResponseNotAllowed(['POST'])


from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            save_image(request, task)
            form.save()

            # Обработка комментариев
            comment_content = request.POST.get('content')
            if comment_content:
                comment = Comment(content=comment_content, task=task, user=request.user)  # Задаем значения для полей task и user
                comment.save()

            return redirect('edit_task', task_id=task_id)
    else:
        form = TaskForm(instance=task)
    comments = task.comments.all()
    return render(request, 'crm/edit_task.html', {'form': form, 'task': task, 'comments': comments})




def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_list')
    else:
        form = TaskForm()
    return render(request, 'crm/edit_task.html', {'form': form})

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

def payment(request):
    tasks = Task.objects.filter(status__name='Checked')
    tasks_by_developer = {}
    total_minutes_by_developer = {}
    total_hours_by_developer = {}
    total_payment_by_developer = {}

    for task in tasks:
        developer = task.assign.username
        if developer not in tasks_by_developer:
            tasks_by_developer[developer] = []
            total_minutes_by_developer[developer] = 0
            total_hours_by_developer[developer] = {
                'hours': 0,
                'minutes': 0
            }
            total_payment_by_developer[developer] = Decimal('0.0')
        tasks_by_developer[developer].append(task)

        if task.estimate_team:
            total_minutes_by_developer[developer] += task.estimate_team
        elif task.estimate_finish:
            total_minutes_by_developer[developer] += task.estimate_finish

        total_hours_by_developer[developer]['hours'] = float(total_minutes_by_developer[developer] / 60)
        total_hours_by_developer[developer]['minutes'] = total_minutes_by_developer[developer]

    total_payment_by_developer = {}

    for developer, hours_minutes in total_hours_by_developer.items():
        bid = Bid.objects.filter(user__username=developer).first()
        if bid:
            payment = round(float(hours_minutes['hours']) * float(bid.payment), 2)
            total_payment_by_developer[developer] = payment

    context = {
        'tasks_by_developer': tasks_by_developer,
        'total_minutes_by_developer': total_minutes_by_developer,
        'total_hours_by_developer': total_hours_by_developer,
        'total_payment_by_developer': total_payment_by_developer,
    }

    if request.user.is_superuser:
        return render(request, 'crm/payment.html', context)
    else:
        return render(request, 'crm/payment.html', context)


