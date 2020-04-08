from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from accounts.models import Profile


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET.get('next'))
            return HttpResponseRedirect(reverse('ticketing:showtime_list'))
        else:
            context = {
                'username': username,
                'error': 'کاربری با این مشخصات یافت نشد'
            }
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('ticketing:showtime_list'))
        context = {}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


@login_required
def profile_details(request):
    try:
        profile = request.user
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    #profile = Profile.objects.create(user=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile_details.html', context)

