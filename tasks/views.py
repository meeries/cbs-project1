from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
import sqlite3

@login_required(login_url='login')
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required(login_url='login')
def task_detail(request, task_id):
# Flaw: Broken Access Control
    task = Task.objects.get(id=task_id) 
    return render(request, 'tasks/task_detail.html', {'task': task})
# Fix: Replace the previous two lines (the function body) with code that includes a check that ensures the task being viewed belongs to the user viewing it:
#   try:
#       task = Task.objects.get(id=task_id, user=request.user) 
#       return render(request, 'tasks/task_detail.html', {'task': task})
#   except Task.DoesNotExist:
#       return redirect('task_list')

# Flaw: CSRF Vulnerability
# Fix: Remove @csrf_exempt to enable Django's CSRF protection
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
# Flaw: (SQL) Injection
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM tasks_task WHERE id = {task_id}")  # BAD: Directly interpolating user input
    conn.commit()
    conn.close()
    return redirect('task_list')
# Fix: Replace the function body with the following code that uses Django's own ORM and deletes the task safely
#    task = Task.objects.get(id=task_id, user=request.user)
#    task.delete()
#    return redirect('task_list')

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