from django.shortcuts import render
from products.models import Product, Category

# Create your views here.

def index(request):
    categories = Category.objects.all()
    names = []
    for category in categories:
        name = category.category_name
        names.append(name)
    print('names : ', names)
    context = {'products': Product.objects.all(), 'category_name': names}
    prods = Product.objects.all()
    for prod in prods:
        print('context is : ', prod.product_images)
    return render(request, 'index.html', context=context)

def category_index(request, slug):
    categories = Category.objects.all()
    names = []
    for cat in categories:
        name = cat.category_name
        names.append(name)
    # print('names : ', names)
    category = Category.objects.get(category_name = slug)
    print('cate : ', category)
    products = Product.objects.filter(category = category)
    print('prod : ', products)
    context = {'products': products, 'category_name': names}
    return render(request, 'index.html', context=context)