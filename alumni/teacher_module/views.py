from django.shortcuts import render, redirect
from .models import Teacher
from alumni_module.models import Alumni
from django.contrib.auth.hashers import check_password

def teacher_login(request):
    error = ""

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            teacher = Teacher.objects.get(username=username)
            if check_password(password, teacher.password):
                request.session['teacher_id'] = teacher.id
                return redirect('/teacher/verify/')
            else:
                error = "Invalid username or password"
        except Teacher.DoesNotExist:
            error = "Invalid username or password"

    return render(request, 'teacher_login.html', {'error': error})


def verify_alumni(request):
    if not request.session.get('teacher_id'):
        return redirect('/teacher/login/')

    alumni = Alumni.objects.filter(is_verified=False)

    if request.method == 'POST':
        alumni_id = request.POST['alumni_id']
        a = Alumni.objects.get(id=alumni_id)
        a.is_verified = True
        a.save()
        return redirect('/teacher/verify/')

    return render(request, 'verify_alumni.html', {'alumni': alumni})


def teacher_logout(request):
    request.session.flush()
    return redirect('/')
