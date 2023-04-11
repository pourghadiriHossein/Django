from django.shortcuts import render, get_object_or_404
from django.urls import resolve
from . import models

def cart(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/cart.html', context)

def checkout(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/checkout.html', context)

def contact(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/contact.html', context)

def frequency_and_answer(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/frequencyAndAnswer.html', context)

def home(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    
    allCategories = models.Categories.objects.all()
    mainCategories = models.Categories.objects.filter(parent_id = None)
    
    latestProduct = models.Products.objects.order_by('-id')[:4]
    
    menCategory = []
    for category in allCategories:
        if category.id == 1 or (category.parent_id != None and category.parent_id.id == 1):
            menCategory.append(category.id)
    latestMenProduct = models.Products.objects.filter(category_id__in=menCategory).order_by('-id')[:6]
    
    WomenCategory = []
    for category in allCategories:
        if category.id == 2 or (category.parent_id != None and category.parent_id.id == 2):
            WomenCategory.append(category.id)
    latestWomenProduct = models.Products.objects.filter(category_id__in=WomenCategory).order_by('-id')[:6]
    
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : mainCategories,
        'latestProduct' : latestProduct,
        'latestMenProduct' : latestMenProduct,
        'latestWomenProduct' : latestWomenProduct,
    }
    return render(request, 'public/home.html', context)    

def product(request, pk):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    current_category = get_object_or_404(models.Categories, pk = pk)
    tags = models.Tags.objects.all()
    allCategories = models.Categories.objects.all()
    menCategory = []
    for category in allCategories:
        if category.id == 1 or (category.parent_id != None and category.parent_id.id == 1):
            menCategory.append(category.id)
    latestMenProduct = models.Products.objects.filter(category_id__in=menCategory).order_by('-id')[:3]
    WomenCategory = []
    for category in allCategories:
        if category.id == 2 or (category.parent_id != None and category.parent_id.id == 2):
            WomenCategory.append(category.id)
    latestWomenProduct = models.Products.objects.filter(category_id__in=WomenCategory).order_by('-id')[:3]
    category_IDs = []
    for category in allCategories:
        if category.id == pk or (category.parent_id != None and category.parent_id.id == pk):
            category_IDs.append(category.id)
    products = models.Products.objects.filter(category_id__in=category_IDs).order_by('-id')
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'current_category' : current_category,
        'tag' : False,
        'tags' : tags,
        'latestMenProduct' : latestMenProduct,
        'latestWomenProduct' : latestWomenProduct,
        'products' : products,
    }
    return render(request, 'public/product.html', context)

def tag(request, pk):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    current_tag = get_object_or_404(models.Tags, pk = pk)
    tags = models.Tags.objects.all()
    allCategories = models.Categories.objects.all()
    menCategory = []
    for category in allCategories:
        if category.id == 1 or (category.parent_id != None and category.parent_id.id == 1):
            menCategory.append(category.id)
    latestMenProduct = models.Products.objects.filter(category_id__in=menCategory).order_by('-id')[:3]
    WomenCategory = []
    for category in allCategories:
        if category.id == 2 or (category.parent_id != None and category.parent_id.id == 2):
            WomenCategory.append(category.id)
    latestWomenProduct = models.Products.objects.filter(category_id__in=WomenCategory).order_by('-id')[:3]
    products = models.Products.objects.filter(tag_id=pk).order_by('-id')
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'current_category' : False,
        'tag' : current_tag,
        'tags' : tags,
        'latestMenProduct' : latestMenProduct,
        'latestWomenProduct' : latestWomenProduct,
        'products' : products,
    }
    return render(request, 'public/product.html', context)

def single_product(request, pk):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    product = get_object_or_404(models.Products, pk = pk)
    comments = models.Comments.objects.filter(product_id=pk)
    latestProduct = models.Products.objects.order_by('-id')[:3]
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories,
        'product' : product,
        'comments' : comments,
        'latestProduct' : latestProduct,
    }
    return render(request, 'public/singleProduct.html', context)

def term_and_condition(request):
    current_url = resolve(request.path_info).url_name
    tags = models.Tags.objects.all()
    categories = models.Categories.objects.filter(parent_id = None)
    context = {
        'urlName': current_url,
        'tags' : tags,
        'categories' : categories
    }
    return render(request, 'public/termAndCondition.html', context)

def dashboard(request):
    current_url = resolve(request.path_info).url_name
    context = {
        'urlName': current_url,
    }
    return render(request, 'dashboard/dashboard.html', context) 