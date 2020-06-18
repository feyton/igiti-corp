from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import Trunc
from django.shortcuts import get_object_or_404, redirect
from store.models import SeedProduct

from .models import Task, Workers


# Create your views here.


@login_required
def remove_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task_qs = Task.objects.filter(user=request.user, status=False)

    if task_qs.exists():
        task = task_qs[0]
        task.delete()
        messages.info(request, 'Task deleted')
        return redirect('profile')
    else:
        messages.info(request, "You don't have a task")
        return redirect('profile')


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


product_data = SeedProduct.objects.annotate(created=Trunc(
    'created_on', 'month')).values('created').annotate(products=Sum('id'))
