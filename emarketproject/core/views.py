from django.shortcuts import render, HttpResponse
from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages
from django.http import JsonResponse

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

def farmer_list(request):
    farmers = Farmer.objects.all()
    context = {
        "farmers": farmers
    }

    return render(request, "core/farmer-list.html", context)


def farmer_details(request, farmerId):
    farmers = Farmer.objects.get(farmerId=farmerId)
    products = Product.objects.filter(farmer=farmers, product_status="published")
    context = {
        "farmers": farmers,
        "products": products
    }

    return render(request, "core/farmer-detail.html", context)

def product_detail(request, productId):
    # Get the product from the database using its ID.
    product = Product.objects.get(productId=productId)
    product_image = product.product_images.all()  
    product = Product.objects.get(productId=productId)
    products = Product.objects.filter(category=product.category).exclude(productId=productId)

    context = {
        "product" : product,
        "product_image": product_image,
        "products":products,
    }

    return render(request,"core/product-detail.html",context)


def default(request):
    categories = Category.objects.all()
    address = Address.objects.get(user=request.user)
    # return {
    #     'categories': categories,
    #     'address': address
    #     }

    context = {
        "address" : address,
        "categories": categories,
    }

    return render(request,"core/product-detail.html",context)

def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})