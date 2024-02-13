from django.shortcuts import render, HttpResponse
from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages


# Create your views here.
def index(request):
    # products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(featured=True, product_status="published")

    context = {
        "products":products
    }
    return render(request, 'core/index.html', context)

def product_list(request):
    products = Product.objects.filter(product_status="published")

    context = {
        "products":products
    }
    return render(request, 'core/product-list.html', context)

def category_list(request):
    categories  = Category.objects.all()

    context = {
        "categories":categories
    }

    return render(request, 'core/category-list.html', context)


def product_list_category(request, categoryId):
    category = Category.objects.get(categoryId=categoryId)
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category":category,
        "products":products
    }
    return render(request, "core/category-product-list.html", context)