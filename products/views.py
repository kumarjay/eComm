from django.shortcuts import render
from products.models import Product, Category
from accounts.models import Cart, CartItems
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        categories = Category.objects.all()
        
        categories_desc = []
        names = []
        print('desc : ', categories_desc)
        for category in categories:
            names.append(category.category_name)
            category.slug = {}
            print('slug :', category.slug)
            category_product = Product.objects.filter(category = category)
            prices = []
            for cat_prod in category_product:
                prices.append(cat_prod.price)
            min_price = min(prices)
            max_price = max(prices)
            category.slug['name'] = category.category_name
            category.slug['image'] = category.category_image
            category.slug['price_range'] = str(min_price) + ' - ' + str(max_price)
            # categories_desc[category]['name'] = category.category_name
            if len(categories_desc) < 5:
                categories_desc.append(category.slug)

        print(categories_desc)
        if request.GET.get('decrease'):
            decrease = request.GET.get('decrease')
            print('dec : ', decrease)
        # print('pp ............: ', product.product_name)
        return render(request, 'product.html', context={'product': product, 'related_product': categories_desc, 'category_name': names})
    except Exception as e:
        print(e)


@login_required
def add_to_cart(request, slug):
    values = 1
    if request.method=='POST':
        # slug = request.POST["slug"]
        values = request.POST["values"]
        print('values : ',  values)
    # print('vksjdsgd-------------', request.user.profile.get_cart_count)
    product = Product.objects.get(slug=slug)
    user = request.user
    print(user)
    # print(product)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = CartItems.objects.create(cart=cart, products=product)
    cart_items.items = values
    total_price = float(product.price) * int(values)
    cart_items.total_price = total_price
    print('total price : ', type(product.price), type(values), type(total_price))
    cart_items.save()
    # print('refresher - > ', request.META)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))