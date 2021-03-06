import base64
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from account.forms import LoginForm, RegistrationForm, UserProfileForm, UserForm
from account.models import UserProfile
from mysite.settings import STATICFILES_DIRS
import uuid


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse('success!')
            else:
                return HttpResponse('false')

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('false')
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, 'account/register.html', {"user_form": user_form, "userprofile_form": userprofile_form})


@login_required()
def myself(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(
        request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    return render(request, 'account/myself.html',
                  {"user": request.user, "userprofile": userprofile})


@login_required(login_url='/account/login/')
def myself_edit(request):
    userprofile = UserProfile.objects.get(user=request.user) if hasattr(
        request.user, 'userprofile') else UserProfile.objects.create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            request.user.email = user_cd['email']
            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']
            userprofile.aboutme = userprofile_cd['aboutme']
            request.user.save()
            userprofile.save()
            return HttpResponseRedirect('/account/myself')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={
            "birth": userprofile.birth,
            "phone": userprofile.phone,
            "aboutme": userprofile.aboutme
        })
        return render(request, 'account/myself_edit.html', {
            "user_form": user_form,
            "userprofile_form": userprofile_form
        })


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userprofile = UserProfile.objects.get(user=request.user.id)
        filename = str(uuid.uuid1()) + '.png'
        filepath = os.path.join(STATICFILES_DIRS[0], 'faces/%s' % filename)
        with open(filepath, 'wb') as fp:
            fp.write(base64.b64decode(D_BASE64(img)))
        userprofile.facename = filename
        userprofile.save()
        return HttpResponseRedirect(request, '/account/myself_edit/', {"facename": filename})
    else:
        return render(request, 'account/imagecrop.html')


def D_BASE64(origStr):
    # base64 decode should meet the padding rules
    if (len(origStr) % 3 == 1):
        origStr += "=="
    elif (len(origStr) % 3 == 2):
        origStr += "="

    origStr = bytes(origStr, encoding='utf8')
    dStr = base64.b64decode(origStr).decode()
    print("BASE64 Decode result is: \n" + dStr)
    return dStr
