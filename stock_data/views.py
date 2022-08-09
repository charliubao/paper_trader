from django.shortcuts import render
from . import scrape
import string
import datetime
import pytz
from django.views.generic import RedirectView
from django.urls import reverse
from .forms import PurchaseForm
from django.utils import timezone
from django.db import models
from accounts.models import Profile, HistoryTrack
from django.contrib import messages

# Create your views here.
stocks = scrape.data['data']['rows']
alphabet = list(string.ascii_uppercase)

def index(request):
    rg_data = red_green(stocks)
    underscores = underscore_names(stocks)
    data = zip(stocks, rg_data, underscores)
    return render(request, 'stock_data/index.html', {
        "data" : data, "alphabet" : alphabet, "now" : time_helper()
    })

def letter(request, letter):
    filtered_data = [x for x in stocks if x['symbol'].startswith(letter)]
    rg_data = red_green(filtered_data)
    underscores = underscore_names(filtered_data)
    data = zip(filtered_data, rg_data, underscores)
    return render(request, 'stock_data/index.html', {
        "data" : data, "alphabet" : alphabet, "now" : time_helper(), 
    })

def time_helper():
    timezone = pytz.timezone('America/New_York')
    time = datetime.datetime.now(tz = timezone)
    return time.strftime("%B %d, %Y %H:%M:%S")

def red_green(nums):
    ls = []
    for row in nums:
        try:
            num = float(row['pctchange'][:-1])
            if(num>=0): ls.append(True)
            else: ls.append(False)

        except:
            ls.append(True)
    return ls

def underscore_names(stocks):
    stocknames = [x['name'] for x in stocks]
    translate_table = str.maketrans({' ': '_', ',': '_', '.':'_', '/':'_'})
    underscore_names = [name.translate(translate_table) for name in stocknames]
    return underscore_names

def item(request, name):
    translate_table = str.maketrans({' ': '_', ',': '_', '.':'_', '/':'_'})
    item_data  = [x for x in stocks if x['name'].translate(translate_table) == name]
    keys = list(item_data[0].keys())
    values = list(item_data[0].values())
    header = item_data[0]['name']
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data.get("quantity")
            price = round(float(item_data[0]['lastsale'][1:]), 2)
            if user_profile.can_purchase(num*price):
                user_profile.withdraw(num*price)
                user_profile.save()
                instance = form.save(commit=False)
                instance.owner = request.user
                instance.name = header
                instance.original_price = price
                instance.price_now = price
                HistoryTrack.objects.create(profile=user_profile, stock=header, original_price=price, total=num*price, purchase_time=instance.purchase_time)
                form.save()
                messages.success(request, 'Purchase Successful!')
                return render(request, 'stock_data/purchase.html', {})
            else:
                messages.error(request, 'Insufficient Funds, Unable to Process Transaction. Please Add Balance') 
                form = PurchaseForm()
                return render(request, 'stock_data/item.html', {
                    "keys" : keys, "values" : values, "now" : time_helper(), "header" : header,  "form" : form
                })
    else:
        form = PurchaseForm()
        return render(request, 'stock_data/item.html', {
            "keys" : keys, "values" : values, "now" : time_helper(), "header" : header,  "form" : form
        })

def search(request):
    if request.method == "POST":
        searched = request.POST['searched'].lower()
        results = [x for x in stocks if x['name'].lower().__contains__(searched)]
        rg_data = red_green(results)
        underscores = underscore_names(results)
        data = zip(results, rg_data, underscores)
        return render(request, 'stock_data/search.html', {
            "searched" : searched, "data" : data
        })
    else: 
        index(request)