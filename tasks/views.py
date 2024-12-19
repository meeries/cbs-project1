from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

# Flaw: CSRF Vulnerability
# Fix: 
# Remove @csrf_exempt to enable Django's CSRF protection
@csrf_exempt
@login_required(login_url='login')
def add_task(request):
    if request.method == 'POST':
        task_text = request.POST.get('task', '')
        due_date = request.POST.get('due_date', None)
        if task_text:
            Task.objects.create(user=request.user, task=task_text, due_date=due_date)
        return redirect('task_list')
    return render(request, 'tasks/add_task.html')

@login_required(login_url='login')
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')