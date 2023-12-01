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



from django.contrib import admin
from .models import DeliveryAddress

@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number', 'city', 'area', 'address', 'landmark', 'user')
    list_filter = ('city',)
    search_fields = ('full_name', 'mobile_number', 'city', 'area', 'address', 'landmark')






from django.contrib import admin
from .models import Order, OrderItem

# Define the OrderItem inline for better representation in the Order admin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'shipping_address', 'order_status', 'created_at', 'updated_at')
    list_filter = ('order_status', 'created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'shipping_address__full_name')  # Add other fields for search if needed
    inlines = [OrderItemInline]

    # Customize the change view
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'total_amount', 'shipping_address', 'order_status', 'shipping_cost')
        }),
        # Add more fieldsets for other information like payment details, etc.
    )

admin.site.register(Order, OrderAdmin)
