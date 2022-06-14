from django.shortcuts import render ,HttpResponseRedirect ,HttpResponse ,redirect , get_object_or_404
from cart.cart import Cart
from .forms import OrderCreate
from .models import Order,OrderItem
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreate(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order , product = item['product'] , quantity=item['quantity'], price = item['price'])
                cart.clear()
                order_created.delay(order.id)
            #return render(request , 'orders/order/created.html',{'order':order})
                request.session['order_id']= order.id
                return redirect(reverse('zarinpal:request'))
    else:
        form = OrderCreate()
    return render(request,'orders/order/create.html',{"form":form,"cart":cart})

@staff_member_required
def admin_order_detail(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    return render(request,'admin/orders/order/detail.html',{'order':order})

@staff_member_required
def admin_order_pdf(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    html = render_to_string("orders/order/pdf.html",{"order":order})
    response = HttpResponse(content_type="application/pdf")
    response['response_disposition'] = f"filename=order{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
