from django.urls import path
from accounts.views import login_page, register_page, cart, remove_cart, checkout_session, payment_successful
from ecomm import settings
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_page, name='login'),
    # path('logout/', handle_logout, name='handle_logout'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='handle_logout'),
    path('register/', register_page, name='register_page'),
    path('cart/', cart, name='cart'),
    path('remove-cart/<cart_uid>/', remove_cart, name='remove_cart'),
    path('checkout-session/', checkout_session, name='checkout_session'),
    path('payment_successful/', payment_successful, name='payment_successful')

]