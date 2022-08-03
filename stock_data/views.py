from django.shortcuts import render
from . import scrape
import string
import datetime
import pytz
from django.views.generic import RedirectView
from django.urls import reverse

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
    translate_table = str.maketrans({' ': '_', ',': '_', '.':'_'})
    underscore_names = [name.translate(translate_table) for name in stocknames]
    return underscore_names

def item(request, name):
    translate_table = str.maketrans({' ': '_', ',': '_', '.':'_'})
    item_data  = [x for x in stocks if x['name'].translate(translate_table) == name]
    keys = list(item_data[0].keys())
    values = list(item_data[0].values())
    header = item_data[0]['name']
    return render(request, 'stock_data/item.html', {
        "keys" : keys, "values" : values, "now" : time_helper(), "header" : header
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