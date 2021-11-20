from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from first_app.models import Topic, Webpage, AccessRecord
from . import forms
from first_app.forms import NewWebpageForm, UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
# def index(request):
#     webpages_list = AccessRecord.objects.order_by('date')
#     date_dict = {'access_records': webpages_list}
#     return render(request, 'first_app/index.html', context=date_dict)

def form_name_view(request):
    form = forms.FormName()
    if request.method == "POST":
        form = forms.FormName(request.POST)

        if form.is_valid():
            # CODE HERE
            print("Validation Success!")
            print(f"Name: {form.cleaned_data['name']}")
            print(f"Email: {form.cleaned_data['email']}")
            print(f"Text: {form.cleaned_data['text']}")

    return render(request,'first_app/form_page.html', {'form':form})

def webpages(request):
    form = NewWebpageForm()

    if request.method == "POST":
        form = NewWebpageForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("Error Form Invalid")
    
    return render(request, 'first_app/webpages.html', {'form': form})


def index(request):
    context_dict = {'text':'hello world', 'number':100}
    return render(request, 'templates/index.html', context_dict)

    
def other(request):
    return render(request, 'templates/other.html')

    
def relative(request):
    return render(request, 'templates/relative_url_templates.html')

def index(request):
    return render(request,'user_authentication/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.error, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'user_authentication/registration.html', {'user_form':user_form, 'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username:{} and password {}".format(username, password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request, 'user_authentication/login.html',{})