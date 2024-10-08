from django.shortcuts import render, redirect
from module_group.models import ModuleGroup, Module
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


# Logout view
@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('main:login')  # Redirect to login page after logout

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')  # Redirect to home or dashboard if already logged in

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('main:home')  # Redirect to home or dashboard after login
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# Home view (for testing login_required)
@login_required
def home_view(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    return render(request, 'home.html', {
        'module_groups': module_groups,
        'modules': modules,
    })


def base_view(request):
    module_groups = ModuleGroup.objects.all()
    modules = Module.objects.all()
    return render(request, 'base.html', {
        'module_groups': module_groups,
        'modules': modules,
    })





