import code
from django.shortcuts import render , redirect
from .models import Coupons
from .forms import CouponsForm
from django.utils import timezone
from django.views.decorators.http import require_POST

# Create your views here.


@require_POST
def apply_coupon(request):
    now = timezone.now()
    form = CouponsForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupons.objects.get(code__iexact=code,valid_from__lte=now,valid_to__gte=now,active=True)
            request.session['coupon_id']= coupon.id
        except:
            request.session['coupon_id'] = None
    return redirect("cart:cart_detail")