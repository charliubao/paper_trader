from django.urls import path
from . import views
import string
import re

stocks = views.stocks
underscored = views.underscore_names(stocks)
stocknames = [x['name'] for x in stocks]

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("tag/<str:letter>", views.letter, name="letter"),
    path("name/<str:name>", views.item, name='item'),
]

