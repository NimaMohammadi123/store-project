from django import forms
from django.forms import Form
from .models import Order

class OrderCreate(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','address','email','post_address','city']
