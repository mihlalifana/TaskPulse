
from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment ,  MoodCheckin
from .forms import AssignmentForm, CustomUserCreationForm, MoodCheckInForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

import random, json


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

# User login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'main/login.html')

# Home page with progress tracking and reminders
def home(request):
    assignments = Assignment.objects.filter(user=request.user)
    due_soon = [a for a in assignments if a.is_due_soon()]
    
    total_tasks = assignments.count()
    completed_tasks = assignments.filter(completed=True).count()
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    return render(request, 'main/home.html', {
        'assignments': assignments,
        'due_soon': due_soon,
        'progress': progress
    })

# Add a new assignment
def add_task(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.user = request.user
            assignment.save()
            return redirect('home')
    else:
        form = AssignmentForm()
    return render(request, 'main/add_task.html', {'form': form})

# View all tasks
def task_list(request):
    assignments = Assignment.objects.filter(user=request.user)
    return render(request, 'main/task_list.html', {'assignments': assignments})

def edit_task(request, task_id):
    task = get_object_or_404(Assignment, id=task_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = AssignmentForm(instance=task)
    return render(request, 'main/edit_task.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

# Delete a task
def delete_task(request, task_id):
    task = get_object_or_404(Assignment, id=task_id)
    task.delete()
    return redirect('task_list')

def calendar_view(request):
    now = timezone.now()
    assignments = Assignment.objects.filter(user=request.user, due_date__gte=now).order_by('due_date')
    return render(request, 'main/calendar.html', {'assignments': assignments})


import random
from django.shortcuts import render
from .models import Assignment

def progress_view(request):
    # Fetch all tasks for the logged-in user
    all_tasks = Assignment.objects.filter(user=request.user)

    # Separate completed and pending tasks
    completed_tasks = all_tasks.filter(completed=True)
    pending_tasks = all_tasks.filter(completed=False)

    # Calculate completion statistics
    total = all_tasks.count()
    completed_count = completed_tasks.count()
    pending_count = pending_tasks.count()
    completion_rate = int((completed_count / total) * 100) if total else 0

    # Contextual motivational tips
    if completion_rate == 100:
        tips = [
            "🎉 Amazing! You’ve completed everything—time to reward yourself!",
            "✅ 100%! Great job staying on track.",
            "You’re crushing it—keep up the momentum!"
        ]
    elif completion_rate >= 70:
        tips = [
            "💪 You’re almost there. Finish strong!",
            "You’ve done a lot already—just a little more!",
            "Keep going! The finish line is in sight."
        ]
    elif completion_rate >= 30:
        tips = [
            "Stay consistent—progress adds up!",
            "Small steps lead to big wins. Keep at it!",
            "Try tackling one more task today—you’ve got this!"
        ]
    elif completion_rate > 0:
        tips = [
            "Every completed task counts. Start with a quick one!",
            "You're off to a good start—keep building momentum!",
            "Don't stop now! Just one more task can make a difference."
        ]
    else:
        tips = [
            "Let’s get started—one small task at a time!",
            "Start now, even if it’s just for 5 minutes.",
            "Taking the first step is the hardest—go for it!"
        ]

    motivational_tip = random.choice(tips)

    # Prepare chart data
    chart_data = {
        'completed_count': completed_count,
        'pending_count': pending_count,
    }

    # Pass context to template
    context = {
        'completed_tasks': completed_tasks.order_by('-due_date'),
        'completed_count': completed_count,
        'pending_count': pending_count,
        'completion_rate': completion_rate,
        'motivational_tip': motivational_tip,
        'chart_data': json.dumps(chart_data),
    }

    return render(request, 'main/progress.html', context)





def mood_checkin(request):
    latest_checkin = MoodCheckin.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        form = MoodCheckInForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            mood_entry.save()
            return render(request, 'main/mood_success.html', {
                'mood': mood_entry.get_mood_display(),
                'message': mood_entry.motivation_message(),
                'note': mood_entry.note,
            })
    else:
        form = MoodCheckInForm()
    
    return render(request, 'main/mood_checkin.html', {
        'form': form,
        'latest_checkin': latest_checkin
    })
