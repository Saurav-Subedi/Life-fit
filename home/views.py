from django.shortcuts import render, redirect
from .forms import DeliveryAddressForm
from .models import ORDER_STATUSES, Cart, Order, OrderItem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import OTP  
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.conf import settings
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Cart, Product
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
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from .models import OrderItem, Cart, Product  # Import your models here

# Rest of your code...


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
        
        totalamount = amount

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

from django.contrib.auth import logout


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
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

from django.shortcuts import render, redirect
from .models import DeliveryAddress
from .forms import DeliveryAddressForm

from home.models import DeliveryAddress


from django.shortcuts import render, redirect


from .models import Cart

def proceed_to_checkout(request):
    user = request.user
    addresses = DeliveryAddress.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.product.selling_price * item.quantity for item in cart_items)
    
    if cart_items.exists():
        totalitem = cart_items.count()
        return render(request, 'app/checkout.html', {
            'addresses': addresses,
            'totalamount': amount,
            'cart_items': cart_items,
            'totalitem': totalitem,
            'nptotal': round(amount / 132, 2),
            'amount': amount
        })
    else:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')



from django.shortcuts import get_object_or_404, redirect, render
from .forms import DeliveryAddressForm
from .models import DeliveryAddress

def add_delivery_address(request):
    user_addresses = DeliveryAddress.objects.filter(user=request.user)
    default_address = user_addresses.filter(is_default=True).first()

    if default_address:
        form = DeliveryAddressForm(request.POST or None, instance=default_address)
    else:
        form = DeliveryAddressForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            if address.is_default:
                user_addresses.exclude(pk=address.pk).update(is_default=False)

            return redirect('proceed_to_checkout')

    return render(request, 'app/add_delivery_address.html', {'form': form})


def edit_delivery_address(request, address_id):
    address = get_object_or_404(DeliveryAddress, pk=address_id, user=request.user)

    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            is_default = request.POST.get('is_default')
            if is_default:
                address.is_default = True
                DeliveryAddress.objects.filter(user=request.user).exclude(pk=address.pk).update(is_default=False)
            else:
                address.is_default = False

            address.save()
            return redirect('proceed_to_checkout')
    else:
        form = DeliveryAddressForm(instance=address)

    return render(request, 'app/edit_delivery_address.html', {'form': form, 'address_id': address_id})



def delete_delivery_address(request, address_id):
    if request.method == 'POST':
        address = get_object_or_404(DeliveryAddress, pk=address_id, user=request.user)
        
        if address:
            address.delete()
            messages.success(request, 'Address deleted successfully.')
    
    return redirect('proceed_to_checkout')  # Redirect to an appropriate URL after address deletion

from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, Order, OrderItem, DeliveryAddress

class PlaceOrderAndPaymentView(View):
    template_name = 'app/place_order.html'

    def get(self, request):
        user = request.user

        # Fetch cart items for the logged-in user
        cart_items = Cart.objects.filter(user=user)
        total_amount = sum(cart_item.product.selling_price * cart_item.quantity for cart_item in cart_items)

        # Fetch all delivery addresses for the logged-in user
        delivery_addresses = DeliveryAddress.objects.filter(user=user)

        return render(request, self.template_name, {
            'cart_items': cart_items,
            'delivery_addresses': delivery_addresses,
            'totalamount': total_amount
        })

    def post(self, request):
        payment_method = request.POST.get('payment_method')
        if payment_method:
            if 'delivery_address_id' in request.POST:
                return self.place_order_from_address(request, payment_method)
            else:
                return self.place_order_with_default_address(request, payment_method)
        else:
            return render(request, self.template_name, {'error_message': 'Please select a payment method.'})

    def create_order(self, user, delivery_address, payment_method, cart_items):
        new_order = Order.objects.create(
            user=user,
            shipping_address=delivery_address,
            order_status='Pending',
            total_amount=0
        )

        total_amount = 0
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=new_order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            total_amount += cart_item.product.selling_price * cart_item.quantity

        new_order.total_amount = total_amount
        new_order.save()

        return new_order

    def place_order_from_address(self, request, payment_method):
        delivery_address_id = request.POST.get('delivery_address_id')
        delivery_address = DeliveryAddress.objects.get(id=delivery_address_id)
        cart_items = Cart.objects.filter(user=request.user)

        new_order = self.create_order(request.user, delivery_address, payment_method, cart_items)
        self.process_cart_and_order(request.user, cart_items, new_order)
        return redirect('order_confirmation')

    def place_order_with_default_address(self, request, payment_method):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        default_address = DeliveryAddress.objects.filter(user=user, is_default=True).first()

        new_order = self.create_order(user, default_address, payment_method, cart_items)
        self.process_cart_and_order(user, cart_items, new_order)
        return redirect('order_confirmation')

    def process_cart_and_order(self, user, cart_items, new_order):
        cart_items.delete()
        return redirect('home')


class OrderConfirmationView(View):
    def get(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        return render(request, 'app/order_confirmation.html', {'cart_items': cart_items})

    def post(self, request):
        place_order_view = PlaceOrderAndPaymentView()

        delivery_address_id = request.POST.get('delivery_address_id')
        if delivery_address_id:
            delivery_address = get_object_or_404(DeliveryAddress, id=delivery_address_id, user=request.user)
            cart_items = Cart.objects.filter(user=request.user)  # Retrieve cart items again

            new_order = place_order_view.create_order(request.user, delivery_address, 'cash_on_delivery', cart_items)
            
            if new_order:
                place_order_view.process_cart_and_order(request.user, cart_items, new_order)
                self.send_confirmation_email(request.user, new_order)  # Sending confirmation email
                cart_items.delete()
                messages.success(request, 'Orders confirmed successfully!')
                return redirect('home')
        
        messages.error(request, 'Order placement was unsuccessful.')
        return redirect('order_confirmation')

    def send_confirmation_email(self, user, order):

        print(f"Email sent to {user.email} for order {order.id} confirmation.")
 
class OrderListView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        
        # Assuming you're retrieving orders related to the current user
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            # Retrieve orders related to the current user and product
            orders = OrderItem.objects.filter(product=product, order__user=request.user).select_related('order')
            
            # Calculate total price for each order item and include order status
            for order_item in orders:
                order_item.total_price = order_item.quantity * order_item.product.selling_price
                order_item.order_status = order_item.order.order_status  # Include order status
                
        else:
            orders = None  # If not authenticated, set orders to None or an empty queryset

        return render(request, 'app/order_list.html', {
            'product': product,
            'item_already_in_cart': item_already_in_cart,
            'totalitem': totalitem,
            'orders': orders,  # Pass the orders related to this product to the template
            'order_statuses': ORDER_STATUSES  # Pass the order statuses to the template
        })
