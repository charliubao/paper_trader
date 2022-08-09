from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from .models import Purchase, Profile, HistoryTrack
from stock_data.views import stocks as data
from django.http import HttpResponse 
from django.utils import timezone

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

@login_required(login_url='login')
def homepage(request):
    request.user.profile.cash = round(float(request.user.profile.cash), 2)
    stocks = Purchase.objects.filter(owner=request.user)
    #udpate stocks to current price
    translate_table = str.maketrans({' ': '_', ',': '_', '.':'_', '/':'_'})
    for stock in stocks:
        item_data  = [x for x in data if x['name'].translate(translate_table) == stock.name]
        if len(item_data) > 0:
            stock.price_now = round(float(item_data[0]['lastsale'][1:]), 2)
    #add total assets
    total = 0
    for stock in stocks:
        total += stock.quantity*stock.price_now
    user_profile = Profile.objects.get(user=request.user)
    total += user_profile.cash
    total = round(float(total), 2)
    return render(request, 'accounts/homepage.html', {
        'stocks': stocks, "total": total
    })

def add_balance(request):
    request.user.profile.cash = round(float(request.user.profile.cash), 2)
    stocks = Purchase.objects.filter(owner=request.user)
    translate_table = str.maketrans({' ': '_', ',': '_', '.':'_', '/':'_'})
    for stock in stocks:
        item_data  = [x for x in data if x['name'].translate(translate_table) == stock.name]
        if len(item_data) > 0:
            stock.price_now = round(float(item_data[0]['lastsale'][1:]), 2)
    total = 0
    for stock in stocks:
        total += stock.quantity*stock.price_now
    user_profile = Profile.objects.get(user=request.user)
    total += user_profile.cash
    total = round(float(total), 2)

    if request.method == 'POST':
        action = request.POST.get('amount')
        user_profile = Profile.objects.get(user=request.user)
        user_profile.deposit(round(float(action), 2))
        HistoryTrack.objects.create(profile=user_profile, stock="Deposit", original_price=round(float(action), 2), total=round(float(action), 2), purchase_time=timezone.now())
        user_profile.save()
    return render(request, 'accounts/add_balance.html', {
        "total": total
    })

def sell(request):
    request.user.profile.cash = round(float(request.user.profile.cash), 2)
    stocks = Purchase.objects.filter(owner=request.user)
    translate_table = str.maketrans({' ': '_', ',': '_', '.':'_', '/':'_'})
    for stock in stocks:
        item_data  = [x for x in data if x['name'].translate(translate_table) == stock.name]
        if len(item_data) > 0:
            stock.price_now = round(float(item_data[0]['lastsale'][1:]), 2)
    total = 0
    for stock in stocks:
        total += stock.quantity*stock.price_now
    user_profile = Profile.objects.get(user=request.user)
    total += user_profile.cash
    total = round(float(total), 2)

    if request.method == 'POST':
        picks = request.POST.get('sell')
        shares = int(request.POST.get('number_to_sell'))
        stock = Purchase.objects.get(name=picks)
        if stock.quantity < shares:
            messages.error(request, 'You do not have that many shares of ' + picks)
        else:
            if stock.quantity > shares:
                stock.quantity -= shares
                stock.save()
                user_profile = Profile.objects.get(user=request.user)
                user_profile.deposit(stock.price_now * shares)
                user_profile.save()
            else: 
                stock.delete()
    return render(request, 'accounts/sell.html', {
        "total": total, "stocks" : stocks
    })

def history(request):
    items = HistoryTrack.objects.filter(profile=request.user.profile)
    return render(request, 'accounts/history.html', {
        "items": items
    })