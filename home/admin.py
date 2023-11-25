from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import *


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    # list_display = ['user', 'id', 'name', 'locality', 'city', 'zipcode', 'state']
    # list_filter = ('user', 'state')
    search_fields = ('name', 'locality', 'city', 'zipcode')
    list_per_page = 8


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title','category','selling_price', 'short_description',
                    'description', 'brand', 'product_image']
    list_filter =('brand','category')
    search_fields =('title','selling_price','description')
    list_per_page = 6

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter =('user','product')
    search_fields =('quantity',)
    list_per_page = 9

# @admin.register(Order)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer_info',
                    'product', 'product_info', 'quantity', 'ordered_date', 'status']
    list_filter = ('user','status','product')
    search_fields = ('quantity','ordered_date')
    list_per_page = 10
    list_editable =('status',)

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin,):
	list_display = ['id', 'token','user', 'verify']
    

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}
    search_fields=['name','slug']

class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp_code', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'user__email')
admin.site.register(OTP, OTPAdmin)



