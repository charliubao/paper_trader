from django import forms
from django.forms import ModelForm
from accounts.models import Purchase


class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ('quantity',)
        labels = {
            'quantity' : 'Number of Shares'
        }
        widgets = {
            'quantity' : forms.NumberInput(attrs={'class' : 'form-control'})
        }