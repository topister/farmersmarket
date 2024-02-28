from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages
from django.http import JsonResponse
from taggit.models import Tag
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string


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
    # product = Product.objects.get(productId=productId)
    
      
    product = Product.objects.get(productId=productId)
    products = Product.objects.filter(category=product.category).exclude(productId=productId)

    product_image = product.product_images.all()


    # getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Get average reviews related to product
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # product review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:  # user is logged
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False





    context = {
        "product" : product,
        "product_image": product_image,
        "products":products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form": review_form,
        "make_review": make_review,

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


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')
    tag = None
    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context={'products':products,
             'tag':tag
             }
    return render(request, 'core/tag_list.html', context)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})

def ajax_add_review(request, productId):
    # product = Product.objects.get(productId=productId)
    print(f"productId: {productId}")


    try:
        product = Product.objects.get(productId=productId)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product=product,
        review=request.POST["review"],
        rating=request.POST["rating"],
    )

    

    context = {
        # "user":review.user.username,
        # "review":review.review,
        # "rating":review.rating,

        "user":user.username,

        "review":request.POST['review'],
        "rating":request.POST['rating'],


    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    
    return JsonResponse(
        {
            'bool':True,
            'context' :context,
            'average_reviews': average_reviews,
        }
    )

def search(request):
    user_querry = request.GET.get('q')
    products = Product.objects.filter(title__icontains=user_querry, description__icontains=user_querry).order_by("-date")

    context = {
        "user_querry":user_querry,
        "products":products,
    }

    return render(request, 'core/search.html', context)


def filter_products_listing(request):
    categories = request.GET.getlist("category[]")
    farmers = request.GET.getlist("farmer[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)


    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct() 
    # else:
    #     products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    if len(farmers) > 0:
        products = products.filter(farmer__farmerId__in=farmers).distinct() 
    # else:
    #     products = Product.objects.filter(product_status="published").order_by("-id").distinct()    
    
       

    
    data = render_to_string("core/filter-products.html", {"products": products})
    return JsonResponse({"data": data})


def add_to_cart(request):
    cartProduct = {}

    cartProduct[str(request.GET['id'])] = {
        'title':request.GET['title'],
        # 'title': request.GET.get('title', 'Default Title'),

        'quantity':request.GET['qty'],
        'price':request.GET['price'],
        'image':request.GET['img'],
        'productId':request.GET['productId'],

    }

    if 'cart_dataObj' in request.session:
        if str(request.GET['id']) in request.session['cart_dataObj']:
            cart_data = request.session['cart_dataObj']
            cart_data[str(request.GET['id'])]['qty'] = int(cartProduct[str(request.GET['id'])]['quantity'])
            
            cart_data.update(cart_data)
            request.session['cart_dataObj'] = cart_data

        else:
            cart_data = request.session['cart_dataObj']
            cart_data.update(cartProduct)
            request.session['cart_dataObj'] = cart_data

    else:
        request.session['cart_dataObj'] = cartProduct

    
    return JsonResponse({"data":request.session['cart_dataObj'], "cartTotalItems":len(request.session['cart_dataObj'])})



def cart_view_homepage(request):
    cart_total_amount = 0
    if 'cart_dataObj' in request.session:
        for product_id, item in request.session['cart_dataObj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

        return render(request, "core/cart.html", {"cart_data":request.session['cart_dataObj'], 'cartTotalItems': len(request.session['cart_dataObj']), 'cart_total_amount':cart_total_amount})
    else:
        messages.warning(request, "Cart is empty!")

        return redirect("core:index")

def delete_cart_item(request):
    product_id = str(request.GET['id'])

    if 'cart_dataObj' in request.session:
        if product_id in request.session['cart_dataObj']:
            cart_data = request.session['cart_dataObj']
            del request.session['cart_dataObj'][product_id]

            request.session['cart_dataObj'] = cart_data

    cart_total_amount = 0
    if 'cart_dataObj' in request.session:
        for productId, item in request.session['cart_dataObj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

    
    context = render_to_string("core/async-cart-list.html", {"cart_data":request.session['cart_dataObj'], 'cartTotalItems': len(request.session['cart_dataObj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'cartTotalItems': len(request.session['cart_dataObj'])})



def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['quantity']

    if 'cart_dataObj' in request.session:
        if product_id in request.session['cart_dataObj']:
            cart_data = request.session['cart_dataObj']
            cart_data[str(request.GET['id'])]['quantity'] = product_qty
            request.session['cart_dataObj'] = cart_data

    cart_total_amount = 0

    if 'cart_dataObj' in request.session:
        for productId, item in request.session['cart_dataObj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

    context = render_to_string("core/async-cart-list.html", {"cart_data":request.session['cart_dataObj'], 'cartTotalItems': len(request.session['cart_dataObj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data": context, 'cartTotalItems': len(request.session['cart_dataObj'])})





