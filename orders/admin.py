from atexit import register
from django.contrib import admin
from .models import Order , OrderItem
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem

def order_detail(obj):
    urls = reverse("orders:admin_order_detail",args=[obj.id])
    return mark_safe(f'<a href="{urls}">view<a>')

def order_pdf(obj):
    urls = reverse("orders:admin_order_pdf",args=[obj.id])
    return mark_safe(f'<a href="{urls}">PDF<a>')

order_pdf.short_description = "export to PDF"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','email','paid',order_detail,order_pdf]
    list_filter = ['paid']
    inlines = [OrderItemInline]