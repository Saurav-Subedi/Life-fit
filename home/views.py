from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from .models import Category, Customer, Cart, Product
from .forms import CustomerRegistrationForm, ForgotPasswordForm, LoginForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from .forms import CustomerRegistrationForm, OTPVerificationForm
from django.core.mail import send_mail
from .models import OTP
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def search_posts(request):
    query = request.GET.get('query')
    results = []

    
    if query:
        results = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(selling_price__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, 'app/search.html', {'query': query, 'results': results})

class CategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        products = category.product_set.all()  
        data = {
            'catData': category,
            'productData': products,
        }
        return render(request, 'app/category.html', data)


class ProductView(View):
    def get(self, request):
        totalitem = 0
        categories = Category.objects.all()
        products = Product.objects.all()

        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()

        return render(request, 'app/home.html', {
            'categories': categories,
            'products': products,
            'totalitem': totalitem,
        })

class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {
            'product': product,
            'item_already_in_cart': item_already_in_cart,
            'totalitem': totalitem
        })


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

from django.http import JsonResponse
from django.db.models import Q
from .models import Cart

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)

        amount = 0.0
        shipping_amount = 60.0
        cart_items = []
        
        for cart_item in cart:
            tempamount = cart_item.quantity * cart_item.product.selling_price
            amount += tempamount
            cart_items.append({
                'cart': cart_item,
                'total_price': tempamount
            })
        
        totalamount = amount + shipping_amount

        return render(request, 'app/addtocart.html', {
            'carts': cart_items,
            'totalamount': totalamount,
            'amount': amount,
            'totalitem': totalitem
        })
    else:
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/emptycart.html', {'totalitem': totalitem})

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Cart  # Import your Cart model here

@login_required
def update_cart(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        action = request.POST.get('action')

        try:
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))

            if action == 'add':
                # Increment the quantity
                cart_item.quantity += 1
            elif action == 'minus':
                # Decrement the quantity, ensuring it doesn't go below 1
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
            cart_item.save()

            # Calculate cart totals
            cart_products = Cart.objects.filter(user=request.user)
            amount = sum(p.quantity * p.product.selling_price for p in cart_products)
            shipping_amount = 60.0
            totalamount = amount + shipping_amount

            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

from django.views.decorators.csrf import csrf_exempt
from .models import Cart  # Import your Cart model


@login_required
@csrf_exempt 
def remove_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            cart_item = Cart.objects.get(id=item_id, user=request.user)
            cart_item.delete()
            return JsonResponse({'message': 'Item removed successfully'})
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found'})
    else:
        pass

def buy_now(request):
    return render(request, 'app/buynow.html')

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import OTP  

class LogInView(View):
    def get(self, request):
        form = LoginForm(request)
        return render(request, 'app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    otp = OTP.objects.get(user=user)
                except OTP.DoesNotExist:
                    otp = None

                if otp and otp.is_verified:
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('home') 
                elif otp and not otp.is_verified:
                    messages.info(request, 'Your account isn\'t verified with OTP. Please check your email.')
                    return redirect('login')
                else:
                    messages.info(request, 'Your account isn\'t verified. Please check your email.')
                    return redirect('login')
            else:
                messages.info(request, 'Invalid username or password.')
                return redirect('app:login')
        else:
             return render(request, 'app/login.html', {'form': form})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if an account with the same email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email address already exists.")
                return redirect('customer_registration')

            new_user = form.save()

            otp = OTP.objects.create(user=new_user)
            otp.generate_otp()
            otp.save()
            send_otp_email(new_user.email, otp.otp_code)
            login(request, new_user)

            messages.success(request, "Your Account Created Successfully. Check your email for OTP.")
            return redirect('otp_verification')
        return render(request, 'app/customerregistration.html', {'form': form})


class OTPVerificationView(View):
    def get(self, request):
        form = OTPVerificationForm()
        return render(request, 'app/otp_verification.html', {'form': form})

    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            user = request.user  # Assuming the user is logged in
            otp = OTP.objects.get(user=user)

            if otp.is_valid(otp_code):
                otp.is_verified = True
                otp.save()
                messages.success(request, "OTP Verified successfully.")
                return redirect('registration_success')
            else:
                messages.error(request, "Invalid OTP. Please try again.")
        return render(request, 'app/otp_verification.html', {'form': form})


def send_otp_email(email, otp_code):
    subject = "OTP Verification Code"
    message = f"Your OTP verification code is: {otp_code}"

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)



def registration_success(request):
    redirect_to = request.GET.get('next', '/')

    if request.user.is_authenticated:
        return redirect(redirect_to)

    if request.method == 'POST':

        username = request.POST['username'] 
        password = request.POST['password'] 

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(redirect_to)
        else:
            pass

    return render(request, 'registration_success.html')

@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    addresses = DeliveryAddress.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]

    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.selling_price
            amount += tempamount
        totalamount = amount  # Remove shipping_amount from the total calculation
        nptotal = round(totalamount / 132, 2)

        if user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=user))
        return render(request, 'app/checkout.html', {
            'addresses': addresses,
            'totalamount': totalamount,
            'cart_items': cart_items,
            'totalitem': totalitem,
            'nptotal': nptotal,
            'amount': amount
        })
    else:
        messages.warning(request, "Please Select your Placed Address.")
        return redirect('/address/')

from django.shortcuts import render, redirect
from .models import DeliveryAddress

def addresses_list(request):
    addresses = DeliveryAddress.objects.filter(user=request.user)
    return render(request, 'app/addresses_list.html', {'addresses': addresses})

def  orders(request):
    pass
