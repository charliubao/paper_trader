from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome Back, ' + username) 
            return redirect('homepage')
        else:
            messages.error(request, 'Trouble Logging In, Try Again') 
            return render(request, 'accounts/login.html', {})
    else:
        return render(request, 'accounts/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, "You have successfully logged out.") 
	return redirect("login")

# def sign_up(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get('username')
#             messages.success(request, 'Account successfully created for ' + user) 
#             return render(request, 'accounts/login.html', {})
#     else:
#         form = UserCreationForm()
#     return render(request, 'accounts/register.html', {
#         "form":form
#     })

@login_required(login_url='login')
def homepage(request):
    return render(request, 'accounts/homepage.html')

        