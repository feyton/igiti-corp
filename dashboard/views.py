from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Trunc
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from store.models import SeedProduct

from .models import Task, Workers

User = get_user_model()


@login_required
def remove_task(request, pk, action):
    task = get_object_or_404(Task, pk=pk)
    task_qs = Task.objects.filter(user=request.user, status=False)

    if task_qs.exists():
        task = task_qs[0]
        ref = task.id
        if action == "delete":
            task.delete()
            messages.info(request, 'Task deleted')
            return JsonResponse({'message': "Task deleted", "id": ref})
        elif action == "completed":
            task.status = True
            task.date_completed = timezone.now()
            task.save()
            return JsonResponse({'message': "Task has been completed", "id": ref})
        else:
            return render(request, "dashboard/includes/forms.html")

    else:
        return JsonResponse({'message': "You don't have a task"})


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_qs = Task.objects.filter(user=request.user, status=False)

    if task_qs.exists():
        task = task_qs[0]
        task.status = True
        task.date_completed = datetime.now()
        task.save()
        messages.info(request, 'Task completed')
        return redirect('profile')
    else:
        messages.info(request, "Not found")
        return redirect('profile')


@login_required
def delete_worker(request, pk):
    worker = Workers.objects.get(id=pk)
    name = worker.full_name

    worker.delete()
    messages.warning(request, '{} - Has been removed'.format(name))
    return redirect('notification')
