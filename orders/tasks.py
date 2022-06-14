from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"number order {order.id} "
    message = f"Dear{order.first_name}thanks for order . order is ready"
    mail_send = send_mail(subject,message,"nima.mohammadi.021@gmail.com",[order.email])
    return mail_send