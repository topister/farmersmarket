from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages, ContactUs
from django.http import JsonResponse
from userauths.models import Profile
from taggit.models import Tag
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.template.loader import render_to_string
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models.signals import post_save


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

@login_required
def checkout(request):

    cart_total_amount = 0
    total = 0

    # checking if cart_dataObj session still exist

    if 'cart_dataObj' in request.session:
        # loop for the total amount for paypal
        for productId, item in request.session['cart_dataObj'].items():
            total += int(item['quantity']) * float(item['price'])

        # creating order object

        order = CartOrder.objects.create(
            user=request.user,
            price=total
        )

        # loop for the cart total amount

        for productId, item in request.session['cart_dataObj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

            cart_order_items = CartItems.objects.create(
                order=order,
                invoice_number="Invoice_NO" + str(order.id),
                item=item['title'],
                image=item['image'],
                quantity=item['quantity'],
                price=item['price'],
                total=float(item['quantity']) * float(item['price']),
            )









    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': 'Order-Item-No' + str(order.id),
        'invoice': 'INV-NO' + str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('core:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('core:paypal-success')),
        'cancel_return': 'http://{}{}'.format(host,reverse('core:paypal-fail')),
            }
    
    # Form to render the paypal button
    payment_button_form = PayPalPaymentsForm(initial=paypal_dict)


    # cart_total_amount = 0

    # if 'cart_dataObj' in request.session:
    #     for productId, item in request.session['cart_dataObj'].items():
    #         cart_total_amount += int(item['quantity']) * float(item['price'])

    try:

        active_address = Address.objects.get(user=request.user, status=True)

    except:
        messages.warning(request, "You have multiple addresses, activate only one!")
        active_address = None


    

    return render(request, "core/checkout.html", {"cart_data":request.session['cart_dataObj'], 'cartTotalItems': len(request.session['cart_dataObj']), 'cart_total_amount':cart_total_amount, 'payment_button_form':payment_button_form, 'active_address':active_address})



@login_required
def paypal_successful(request):

    cart_total_amount = 0

    if 'cart_dataObj' in request.session:
        for productId, item in request.session['cart_dataObj'].items():
            cart_total_amount += int(item['quantity']) * float(item['price'])

    return render(request, 'core/paypal-success.html',  {'cart_data':request.session['cart_dataObj'],'cartTotalItems':len(request.session['cart_dataObj']),'cart_total_amount':cart_total_amount})

@login_required
def paypal_failed(request):
    return render(request, 'core/paypal-fail.html')


# General dashboard


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models.functions import ExtractMonth
from django.db.models import Count
import calendar

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponse("User not authenticated.")

    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)
    
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Handle the case where the profile does not exist for the user
        # You might want to create a new profile or redirect to a profile creation page
        return HttpResponse("Profile does not exist for this user.")

    cart_orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')

    month = []
    total_orders = []

    for order in cart_orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])

    if request.method == 'POST':
        country = request.POST.get('country')
        city = request.POST.get('city')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        new_address = Address.objects.create(
            country=country,
            city=city,
            address=address,
            mobile=mobile,
            user=request.user,
        )
        messages.success(request, "Address saved successfully!")
        return redirect('core:dashboard')
    else:
        # Handle other cases if needed
        pass

    context = {
        "orders": orders,
        "address": address,
        'profile': profile,
        'cart_orders': cart_orders,
        'month': month,
        'total_orders': total_orders,
    }
    return render(request, 'core/dashboard.html', context)

# def dashboard(request):
#     orders = CartOrder.objects.filter(user=request.user).order_by('-id')
#     address = Address.objects.filter(user=request.user)
#     profile = Profile.objects.get(user=request.user)

#     cart_orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')

#     month = []
#     total_orders = []

#     for order in cart_orders:
#         month.append(calendar.month_name[order['month']])
#         total_orders.append(order['count'])



#     if request.method == 'POST':
#         country = request.POST.get('country')
#         city = request.POST.get('city')
#         address = request.POST.get('address')
#         mobile = request.POST.get('mobile')


#         new_address = Address.objects.create(
#             country = country,
#             city = city,
#             address = address,
#             mobile = mobile,
#             user=request.user,
            

#         )
#         messages.success(request, "Address saved successfully!")
#         return redirect('core:dashboard')
#     else:('Error')


#     context = {
#         "orders": orders,
#         "address":address,
#         'profile':profile,
#         'cart_orders':cart_orders,
#         'month':month,
#         'total_orders':total_orders,
        
#     }
#     return render(request, 'core/dashboard.html', context)

# Buyers dashboard
def buyer_dashboard(request):
    return render(request, 'core/buyer-dashboard.html')

# Farmers/any seller dashboard
def seller_dashboard(request):
    return render(request, 'core/seller-dashboard.html')


def view_order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products =  CartItems.objects.filter(order=order)

    context = {
        "products": products,
    }
    return render(request, 'core/order-detail.html', context)

def default_address(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean':True})



@login_required
def wishlist(request):
    wishlist = Wishlist.objects.all()
    context = {
        "w":wishlist
    }
    return render(request, "core/wishlist.html", context)

@login_required
def add_to_wishlist(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(id=product_id)
    context = {}
    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    if wishlist_count > 0:
        context = {
        'bool':False
        }
    else:
        new_wishlist = Wishlist.objects.create(
        product=product,
        user=request.user
        )
        context = {
        'bool':True
        }
    return JsonResponse(context)


@login_required
def wishlist_remove(request):
    wishlist_id = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)
    product  = Wishlist.objects.get(id=wishlist_id)
    product.delete()

    context = {
        'bool': True,
        'w':wishlist,

    }

    wishlist_json = serializers.serialize('json', wishlist)

    data = render_to_string('core/wishlist-items.html', context)
    return JsonResponse({'data':data, 'w': wishlist_json})

def contact(request):
    return render(request, 'core/contactUs.html')

def contact_ajax(request):
    fullname = request.GET['fullname']
    email = request.GET['email']
    phone = request.GET['phone']
    message = request.GET['message']
    subject = request.GET['subject']


    contact = ContactUs.objects.create(
        fullname = fullname,
        email = email,
        phone = phone,
        message = message,
        subject = subject,


    )

    context = {
        'bool':True,
        'message':'Message sent successfully',

    }


    return JsonResponse({'context': context})
