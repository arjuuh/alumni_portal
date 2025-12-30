from django.shortcuts import render, redirect
from alumni_module.models import Alumni

def verify_alumni(request):
    alumni = Alumni.objects.filter(is_verified=False)

    if request.method == 'POST':
        alumni_id = request.POST['alumni_id']
        a = Alumni.objects.get(id=alumni_id)
        a.is_verified = True
        a.save()
        return redirect('/teacher/verify/')

    return render(request, 'verify_alumni.html', {'alumni': alumni})
