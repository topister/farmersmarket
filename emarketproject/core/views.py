from django.shortcuts import get_object_or_404, render
from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages
from django.http import JsonResponse
from taggit.models import Tag
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist


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




    context = {
        "product" : product,
        "product_image": product_image,
        "products":products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form": review_form,
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
        "user":review.user.username,
        "review":review.review,
        "rating":review.rating,

        # "user":user.username,

        # "review":request.POST['review'],
        # "rating":request.POST['rating'],


    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    
    return JsonResponse(
        {
            'bool':True,
            'context' :context,
            'average_reviews': average_reviews,
        }
    )

