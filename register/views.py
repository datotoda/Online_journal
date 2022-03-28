from random import randint

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from .forms import RegistrationForm, ProfileChangeForm
from .models import RegisterCode


def __generate_codes():
    if RegisterCode.objects.filter(used=False).count() == 0:
        RegisterCode.objects.bulk_create([RegisterCode(code=randint(100000, 999999)) for i in range(2, 31)])


def registration(request):
    __generate_codes()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            temp_obs = RegisterCode.objects.filter(used=False, code=int(request.POST['code']))
            if temp_obs:
                temp_ob = temp_obs.first()
                temp_ob.used = True
                temp_ob.save()

                form.save()
                return LoginView.as_view()(request)
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'register/registration.html', context)


def profile(request):
    __generate_codes()

    form = ProfileChangeForm(instance=request.user)
    context = {
        'form': form
    }
    if request.user.is_superuser:
        context['code'] = RegisterCode.objects.filter(used=False).order_by('id').first().code
    return render(request, 'register/profile.html', context)


def profile_update(request):
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        print('form is not valid')

    return redirect('profile')
