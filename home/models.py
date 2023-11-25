from django.db import models
from django.contrib.auth.models import User
import random


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model

class Brand(models.Model):
    name = models.CharField(max_length=80, null=False, blank=False)
    def __str__(self):
        return (self.name)
    
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    short_description = models.TextField(max_length=210)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    product_image = models.ImageField(upload_to='productimg', null=False , blank=False)

    def __str__(self):
        return str(self.id)

class ProductQuantity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - {self.quantity}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    @property
    def totalCost(self):
        return self.quantity * self.product.selling_price
    def __str__(self):
        return str(self.id)



STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class Verification(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=150)
	verify = models.BooleanField(default=False)
    

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    def generate_otp(self):
        self.otp_code = str(random.randint(100000, 999999))
    
    def is_valid(self, otp):
        return self.otp_code == otp




class ResetPasswordToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=32, blank=True, null=True)


    def __str__(self):
        return self.user.username

class DeliveryAddress(models.Model):
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    address = models.TextField()
    landmark = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False) 

    def __str__(self):
        return self.full_name

