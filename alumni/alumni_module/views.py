from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import Alumni

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        batch = request.POST['batch']
        department = request.POST['department']

        Alumni.objects.create(
            name=name,
            email=email,
            password=password,
            batch=batch,
            department=department,
            is_verified=False
        )
        return redirect('/')

    return render(request, 'register.html')


def alumni_list(request):
    alumni = Alumni.objects.filter(is_verified=True)
    return render(request, 'alumni_list.html', {'alumni': alumni})

def alumni_login(request):
    error = ""

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            alumni = Alumni.objects.get(email=email, is_verified=True)
            if check_password(password, alumni.password):
                request.session['alumni_id'] = alumni.id
                return redirect('/dashboard/')
            else:
                error = "Invalid email or password"
        except Alumni.DoesNotExist:
            error = "Invalid email or password or not verified"

    return render(request, 'alumni_login.html', {'error': error})


def dashboard(request):
    alumni_id = request.session.get('alumni_id')

    if not alumni_id:
        return redirect('/login/')

    alumni = Alumni.objects.get(id=alumni_id)
    return render(request, 'dashboard.html', {'alumni': alumni})

def logout_view(request):
    request.session.flush()
    return redirect('/')

