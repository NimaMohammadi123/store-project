from django.contrib import admin
from .models import Coupons

# Register your models here.

@admin.register(Coupons)
class AdminCoupons(admin.ModelAdmin):
    list_display = ['code','valid_from','valid_to','discount','active']
    list_filter = ['active','discount']
    search_field = ["coupon"]