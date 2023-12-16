from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from accounts.models import Cart, CartItems, Profile
from products.models import Category, Product
from django.contrib.auth import authenticate, login, logout
import stripe
from ecomm import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

stripe_key = settings.STRIPE_SECRET_KEY

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            print('user : ', user)
            print('user : ', user.password)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print('user : ', user)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            not_user = "User not Found"
            context = {'not_user': not_user}
            return render(request, 'accounts/login.html', context=context)
    else:
        return render(request, 'accounts/login.html')

def handle_logout(request):
    print('logging out')
    if request.method =='POST':
        logout(request)
        messages.success(request, 'Successfully Logged Out')
        return redirect('/') 
    return HttpResponse('handle_logout')
    
# def register_page(request):
#     return render(request, 'accounts/register.html')

def register_page(request):
    print('testing........', request.method)
    print('xx : ', request.POST.get('username'))
    if request.method == 'POST':
        first_name = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            password_error = 'Both passwords are not matching'
            context = {'pass_mismatch': password_error}
            return render(request, 'accounts/register.html', context=context)
        else:

            user_obj = User.objects.filter(email = email)
            if user_obj.exists():
                messages.warning(request, 'User Exists')
                return HttpResponseRedirect(request.path_info)

            user_obj = User.objects.create(first_name=first_name,
                                        username= first_name + '~' + email,
                                        email=email,
                                        last_name=address)
            user_obj.set_password(password1)
            # cart, _ = Cart.objects.get_or_create(user=user_obj, is_paid=False)
            profile = Profile.objects.create(user=user_obj, is_email_verified=True,
                                                email_token=email)
            print('profile :', profile)
            # print(name, email, phone, password)
            user_obj.save()
            # print(name, email, phone, password)
            messages.warning(request, 'User Created')
            # return HttpResponseRedirect(request.path_info)
        
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/register.html')


def remove_cart(request, cart_uid, item):
    print('slug : ', cart_uid)
    cart_item = CartItems.objects.get(uid=cart_uid)
    product = cart_item.products
    avail_item = product.total_items + int(float(item))
    product.total_items = avail_item
    product.save()
    cart_item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def cart(request):
    user = request.user
    if not user.username:
        first_name = None
    else:
        first_name = user.first_name
    categories = Category.objects.all()
    products = Product.objects.all()
    names = []
    for cat in categories:
        name = cat.category_name
        names.append(name)
    carts = Cart.objects.filter(is_paid=False, user=request.user)
    if carts:
        cart_items = CartItems.objects.filter(cart=carts[0])
        print('len :', len(carts))
        if len(cart_items)>0:
            
            total_price = 0
            category_items = []
            product_items = None
            for c_item in cart_items:
                price = c_item.products.price
                total_item = c_item.items
                product_name = c_item.products.product_name
                category_name = c_item.products.category.category_name
                category_item = Category.objects.get(category_name= category_name)
                print('items : ', category_item)
                product_items = Product.objects.filter(category = category_item)
                print('cat :  ', product_items)
                category_items.append(category_item)

                if total_item is None:
                    total_item = 1
                # print(total_item, ' ', price)
                price = total_item * price
                total_price += price
            context = {'cart': cart_items, 'total_price': total_price, 'recommends': product_items,
                    'category_name': names, 'first_name':first_name}
            # print('context : ', cart_items[0].products.product_name)
            return render(request, 'cart.html', context=context)
        return redirect('/') 
    else:
        return redirect('/') 


def checkout_session(request):
    carts = Cart.objects.filter(is_paid=False, user=request.user)
    cart_items = CartItems.objects.filter(cart=carts[0])
    total_price = 0
    for items in cart_items:
        price = items.products.price
        total_price += price
    stripe.api_key = settings.STRIPE_SECRET_KEY
    print('key :', cart)
    # plan = models.
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data':{
                'currency':'inr',
                'product_data':{
                    'name':'title',
                },
                'unit_amount':total_price * 100,
            },
            'quantity':1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/accounts/payment_successful?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/accounts/cart/'
    )
    print('sess : ', session)
    return redirect(session.url, code=303)


def payment_successful(request):
    # print('check payment', request.user)
    # checkout_session_id = request.GET.get('session_id', None)
    # print('id : ', checkout_session_id, request)
    # session = stripe.checkout.Session.retrieve(checkout_session_id)
    # print('ses : ', session)
    # customer = stripe.Customer.retrieve(session.get('customer_details', {}).get('email', ''))
    # customer = session.get('customer_details', {}).get('email', '')
    # print('cust :', customer)
    # print('user :', request.user)
    user_obj = User.objects.filter(username = request.user)
    # print('user, ', user_obj)
    # print('user :', request.user)
    cart = Cart.objects.filter(is_paid=False, user = request.user)[0]
    # print('cart : ', cart)
    # cart = Cart.objects.create(is_paid = True)
    cart.is_paid = True
    cart.save()
    # print('cart : ', cart)
    # user_id = request.user.user_id
    # print('user id : ',user_id)
    return redirect('/')
        
