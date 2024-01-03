from django.conf import settings
from django.conf.urls.static import static
from django.urls import  path
from home import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView 
from .forms import LoginForm, MyPasswordChangeForm
from .views import CustomerRegistrationView, LogOutView, OTPVerificationView, OrderConfirmationView, OrderListView, PlaceOrderAndPaymentView, ProductDetailView, add_delivery_address, delete_delivery_address, edit_delivery_address  # Import the ForgotPasswordView



urlpatterns = [
    path('search/', views.search_posts, name='search'),
    path('', views.ProductView.as_view(), name="home"),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('register/', CustomerRegistrationView.as_view(), name='customer_registration'),
    path('otp-verification/', OTPVerificationView.as_view(), name='otp_verification'),
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>',
         views.ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug>/', views.CategoryView.as_view(), name='category'),

    path('registration/', views.CustomerRegistrationView.as_view(),name='customerregistration'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('accounts/login/', views.LogInView.as_view(), name='login'),

    path('logout/', LogOutView.as_view(), name='logout'), 

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),

    # path('checkout/', views.checkout, name='checkout'),
    # path('paymentdone/', views.payment_done, name='paymentdone'),
    # path('orders/', views.orders, name='orders'),

    path('proceed-to-checkout/', views.proceed_to_checkout, name='proceed_to_checkout'),


    path('buy/', views.buy_now, name='buy-now'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('add_address/', views.add_address, name='add_address'),
    # path('choose-payment-method/', views.choose_payment_method, name='choose-payment-method'),
    # path('order-summary/', views.order_summary, name='order-summary'),

    path('add_delivery_address/', add_delivery_address, name='add_delivery_address'),
    path('edit_delivery_address/<int:address_id>/', edit_delivery_address, name='edit_delivery_address'),
    path('delete_delivery_address/<int:address_id>/', delete_delivery_address, name='delete_delivery_address'),
    
    path('placeorder/', PlaceOrderAndPaymentView.as_view(), name='placeorder'),

    path('order_confirmation/', OrderConfirmationView.as_view(), name='order_confirmation'),
    path('orders/<int:pk>/', OrderListView.as_view(), name='order_list'),  # URL for OrderListView

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

