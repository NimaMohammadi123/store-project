from email import message
from django.core.mail import EmailMessage
from io import BytesIO
from celery import shared_task
from orders.models import Order
from django.template.loader import render_to_string
from django.conf import settings
import weasyprint


@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"order number{order_id}"
    message = "thanks for order file is attach"
    email = EmailMessage(subject,message,"nima.mohammadi.021@gmail.com",[order.email])
    html = render_to_string("orders/order/pdf.html",{"order":order})
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT+"css/pdf.css")]
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out,stylesheets)
    email.attach(f"order{order_id}",out.getvalue(),"application/pdf")
    email.send()