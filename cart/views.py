from django.shortcuts import render ,redirect , get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import Product_Add_Form
from shop.models import Product
from coupons.forms import CouponsForm
# Create your views here.

@require_POST
def cart_add(request,product_id):
    cart =Cart(request)
    product = get_object_or_404(Product , id =product_id)
    form = Product_Add_Form(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],override_quantity=['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Product,id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart =Cart(request)
    coupon_form = CouponsForm()
    for item in cart:
        item['update_quantity_form']= Product_Add_Form(initial={
            'quantity':item['quantity'],
            'override':True
        })
    return render(request,'cart/detail.html',{"cart":cart,"coupon_form":coupon_form})