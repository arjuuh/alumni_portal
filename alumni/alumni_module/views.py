from django.shortcuts import render, redirect
from .models import Alumni

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        batch = request.POST['batch']
        department = request.POST['department']

        Alumni.objects.create(
            name=name,
            email=email,
            batch=batch,
            department=department,
            is_verified=False
        )
        return redirect('/')

    return render(request, 'register.html')

def alumni_list(request):
    alumni = Alumni.objects.filter(is_verified=True)
    return render(request, 'alumni_list.html', {'alumni': alumni})