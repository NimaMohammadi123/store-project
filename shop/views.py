from gettext import translation
from django.shortcuts import render , get_object_or_404
from .models import Category , Product
from cart.forms import Product_Add_Form

# Create your views here.

def product_list(request , category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        language = request.LANGUAGE_CODE
        category =get_object_or_404(Category , translations__language_code=language ,translations__slug = category_slug)
        products = Product.objects.filter(category =category)
    
    context ={
        "category":category,
        "products":products,
        "categories":categories,
    }
    
    return render(request , 'shop/product/list.html' , context)

def product_detail(request,id,slug):
    language = request.LANGUAGE_CODE
    products = get_object_or_404(Product , id=id ,translations__language_code=language , translations__slug = slug)
    cart_form = Product_Add_Form()
    return render(request , 'shop/product/detail.html' , {"products":products , "form":cart_form})