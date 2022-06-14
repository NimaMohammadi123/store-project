from django.shortcuts import render , get_object_or_404
from orders.models import Order
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from zeep import Client
from .tasks import payment_completed
from cart import cart


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
amount = 1000  # Toman / Required
description = "درکاه پرداخت فروشگاه"  # Required
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/zarinpal/verify/' # Important: need to edit for realy server.

def send_request(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    total_cost = order.total_cost()
    result = client.service.PaymentRequest(MERCHANT, total_cost, description, order.email, "mobile", CallbackURL)
    if result.Status == 100:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    if request.GET.get('Status') == 'OK':
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order,id=order_id)
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            #return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
            order.paid = True
            order.save()
            payment_completed.delay(order.id)
            return render(request,'zarinpal/succes.html',{'id':str(result.RefID)})
        elif result.Status == 101:
           # return HttpResponse('Transaction submitted : ' + str(result.Status))
            return render(request,'zarinpal/succes.html',{'status':str(result.Status)})
        else:
            #main
            #return render(request,'zarinpal/faile.html',{'status':str(result.Status)})
            
            #test
            order.paid = True
            order.save()
            return render(request,'zarinpal/succes.html',{'id':str(result.RefID)})
    else:
        return render(request,'zarinpal/cancel.html',{})
