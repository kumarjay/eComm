from django.shortcuts import render
from products.models import Product, Category, ProductImage
from home.models import BannerImage
from django.http import HttpResponseRedirect

# Create your views here.

def get_custome_product_list(prods):
    all_prods = []
    for prod in prods:
        prod_image = ProductImage.objects.get(product = prod)
        items = {}
        items['product_name'] = prod.product_name
        items['product_description'] = prod.product_description
        items['price'] = prod.price
        items['slug'] = prod.slug
        items['total_items'] = prod.total_items
        items['image'] = prod_image.image

        price = prod.price
        extra_price = price *110 /100
        
        items['price'] = price
        items['extra_price'] = extra_price
        all_prods.append(items)
    return all_prods


def index(request):
    categories = Category.objects.all()
    user = request.user
    if not user.username:
        first_name = None
    else:
        first_name = user.first_name
    
    names = []
    for category in categories:
        name = category.category_name
        names.append(name)
    
    prods = Product.objects.all()
    banner_images = BannerImage.objects.all()
    all_prods = get_custome_product_list(prods)
    context = {'products': all_prods, 'category_name': names, 'banners': banner_images, 'first_name':first_name}
    return render(request, 'index.html', context=context)

def category_index(request, slug):
    user = request.user
    if not user.username:
        first_name = None
    else:
        first_name = user.first_name
    categories = Category.objects.all()
    names = []
    for cat in categories:
        name = cat.category_name
        names.append(name)
    category = Category.objects.get(category_name = slug)
    banner_images = BannerImage.objects.all()
    print('cate : ', category)
    products = Product.objects.filter(category = category)
    print('all prod : ', len(products))
    all_prods = get_custome_product_list(products)
    
    context = {'products': all_prods, 'category_name': names, 'banners': banner_images, 'first_name':first_name}
    return render(request, 'index.html', context=context)

def about(request):
    categories = Category.objects.all()
    user = request.user
    if not user.username:
        first_name = None
    else:
        first_name = user.first_name
    names = []
    for category in categories:
        name = category.category_name
        names.append(name)
    print('about : ', request.META.get('HTTP_REFERER'))
    context = {'category_name': names, 'first_name':first_name}
    return render(request, 'about.html', context=context)