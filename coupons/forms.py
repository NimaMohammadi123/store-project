from django import forms
from django.utils.translation import gettext_lazy as _

class CouponsForm(forms.Form):
    code = forms.CharField(label=_("Coupon"))