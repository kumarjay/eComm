from django.shortcuts import render
from products.models import Product, Category
from accounts.models import Cart, CartItems
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def get_product(request, slug):
    try:
        user = request.user
        if not user.username:
            first_name = None
        else:
            first_name = user.first_name
        product = Product.objects.get(slug=slug)
        categories = Category.objects.all()
        # print('cat :', categories)

        print('desc : ', product.product_description)
        
        categories_desc = []
        names = []
        # print('desc : ', categories_desc)
        for category in categories:
            names.append(category.category_name)
            category.slug = {}
            # print('name :', category.category_name)
            category_product = Product.objects.filter(category = category)
            prices = []
            for cat_prod in category_product:
                prices.append(cat_prod.price)
                # print('price :', prices)
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                category.slug['price_range'] = str(min_price) + ' - ' + str(max_price)
            category.slug['name'] = category.category_name
            category.slug['image'] = category.category_image
            
            # categories_desc[category]['name'] = category.category_name
            if len(categories_desc) < 4:
                categories_desc.append(category.slug)

        # print('desc :', categories_desc)
        # if request.GET.get('decrease'):
        #     decrease = request.GET.get('decrease')
        #     print('dec : ', decrease)
        # print('pp ............: ', product.product_name)
        return render(request, 'product.html', context={'product': product, 'related_product': categories_desc, 'category_name': names, 'first_name':first_name})
    except Exception as e:
        print(e)


@login_required
def add_to_cart(request, slug):
    user = request.user
    if not user.username:
        first_name = None
    else:
        first_name = user.first_name
    values = 1
    if request.method=='POST':
        # slug = request.POST["slug"]
        values = request.POST["values"]
        print('values : ',  values)
    # print('vksjdsgd-------------', request.user.profile.get_cart_count)
    product = Product.objects.get(slug=slug)
    print('prod : ', product.total_items)
    if product.total_items is None:
        print('entr')
        available_item = 1
    else:
        available_item = product.total_items
    print('avil :', available_item)
    total_items = available_item - int(values)
    print('tot :', total_items)
    if total_items < 0:
        print('v sjhdvjhs', request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + f'?alert=danger&items={product.total_items}')
    else:
        user = request.user
        print(user)
        # print(product)
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
        cart_items = CartItems.objects.create(cart=cart, products=product)
        cart_items.items = values
        total_price = float(product.price) * int(values)
        cart_items.total_price = total_price
        # print('total price : ', type(product.price), type(values), type(total_price))
        cart_items.save()
        product.total_items = total_items
        product.save()
        # print('refresher - > ', request.META)
        redirect_url = request.META.get('HTTP_REFERER').split('?')[0]

        return HttpResponseRedirect(redirect_url)