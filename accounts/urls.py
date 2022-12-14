from django.urls import path
from . import views
from .views import UserRegisterView

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('homepage/', views.homepage, name="homepage"),
    path("logout/", views.logout_user, name= "logout"),
    path("add_balance/", views.add_balance, name= "add_balance"),
    path("sell/", views.sell, name= "sell"),
    path("history/", views.history, name= "history"),
]