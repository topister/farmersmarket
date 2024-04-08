from ast import Module
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import requests
from core.models import Applicant, BookmarkProject, Buyer, Project, Product, Category,ProjectCategory, Farmer, Expert, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages, ContactUs
from django.http import JsonResponse
from core.permission import user_is_farmer, user_is_buyer
from userauths.models import Profile
from taggit.models import Tag
from django.db.models import Count, Avg
from core.forms import ProjectApplyForm, ProjectBookmarkForm, ProjectEditForm, ProjectForm, ProductReviewForm
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

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import razorpay
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages



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

def buyer_list(request):
    buyers = Buyer.objects.all()
    context = {
        "buyers": buyers
    }

    return render(request, "core/buyer-list.html", context)

def expert_list(request):
    experts = Expert.objects.all()
    context = {
        "experts": experts
    }

    return render(request, "core/expert-list.html", context)


def farmer_details(request, farmerId):
    farmers = Farmer.objects.get(farmerId=farmerId)
    products = Product.objects.filter(farmer=farmers, product_status="published")
    context = {
        "farmers": farmers,
        "products": products
    }

    return render(request, "core/farmer-detail.html", context)

def buyer_details(request, buyerId):
    buyers = Buyer.objects.get(buyerId=buyerId)
    # products = Product.objects.filter(farmer=farmers, product_status="published")
    context = {
        "buyers": buyers,
        
    }

    return render(request, "core/buyer-detail.html", context)

def expert_details(request, expertId):
    experts = Expert.objects.get(expertId=expertId)
    # products = Product.objects.filter(farmer=farmers, product_status="published")
    context = {
        "experts": experts,
        
    }

    return render(request, "core/expert-detail.html", context)

def product_detail(request, productId): 
      
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

# @login_required
# def checkout(request):

#     cart_total_amount = 0
#     total = 0

#     # checking if cart_dataObj session still exist

#     if 'cart_dataObj' in request.session:
#         # loop for the total amount for paypal
#         for productId, item in request.session['cart_dataObj'].items():
#             total += int(item['quantity']) * float(item['price'])

#         # creating order object

#         order = CartOrder.objects.create(
#             user=request.user,
#             price=total
#         )

#         # loop for the cart total amount

#         for productId, item in request.session['cart_dataObj'].items():
#             cart_total_amount += int(item['quantity']) * float(item['price'])

#             cart_order_items = CartItems.objects.create(
#                 order=order,
#                 invoice_number="Invoice_NO" + str(order.id),
#                 item=item['title'],
#                 image=item['image'],
#                 quantity=item['quantity'],
#                 price=item['price'],
#                 total=float(item['quantity']) * float(item['price']),
#             )

#     host = request.get_host()
#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': cart_total_amount,
#         'item_name': 'Order-Item-No' + str(order.id),
#         'invoice': 'INV-NO' + str(order.id),
#         'currency_code': 'USD',
#         'notify_url': 'http://{}{}'.format(host,reverse('core:paypal-ipn')),
#         'return_url': 'http://{}{}'.format(host,reverse('core:paypal-success')),
#         'cancel_return': 'http://{}{}'.format(host,reverse('core:paypal-fail')),
#             }
    
#     # Form to render the paypal button
#     payment_button_form = PayPalPaymentsForm(initial=paypal_dict)

#     try:

#         active_address = Address.objects.get(user=request.user, status=True)

#     except:
#         messages.warning(request, "You have multiple addresses, activate only one!")
#         active_address = None


    

#     return render(request, "core/checkout.html", {"cart_data":request.session['cart_dataObj'], 'cartTotalItems': len(request.session['cart_dataObj']), 'cart_total_amount':cart_total_amount, 'payment_button_form':payment_button_form, 'active_address':active_address})

@login_required
def checkout(request):

    cart_total_amount = 0
    total = 0
    order = None  # Initialize order outside the if condition

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
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('core:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('core:paypal-success')),
        'cancel_return': 'http://{}{}'.format(host, reverse('core:paypal-fail')),
    }

    # If order is not None (i.e., it was created)
    if order:
        paypal_dict.update({
            'item_name': 'Order-Item-No' + str(order.id),
            'invoice': 'INV-NO' + str(order.id),
        })

    # Form to render the PayPal button
    payment_button_form = PayPalPaymentsForm(initial=paypal_dict)

    try:
        active_address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
        messages.warning(request, "You have multiple addresses, activate only one!")
        active_address = None

    return render(request, "core/checkout.html", {
        "cart_data": request.session.get('cart_dataObj', {}),
        'cartTotalItems': len(request.session.get('cart_dataObj', {})),
        'cart_total_amount': cart_total_amount,
        'payment_button_form': payment_button_form,
        'active_address': active_address
    })


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



def about_us(request):
    return render(request, "core/about_us.html")


def purchase_guide(request):
    return render(request, "core/purchase_guide.html")

def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

def terms_of_service(request):
    return render(request, "core/terms_of_service.html")

# Project part
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.serializers import serialize
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# from account.models import User
from userauths.models import User


from django.http import HttpRequest, JsonResponse

def home_view(request):

    published_projects = Project.objects.filter(is_published=True).order_by('-timestamp')
    projects = published_projects.filter(is_closed=False)
    total_candidates = User.objects.filter(role='farmer').count()
    total_companies = User.objects.filter(role='buyer').count()
    paginator = Paginator(projects, 3)
    page_number = request.GET.get('page', None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        project_lists = []
        project_objects_list = page_obj.object_list.values()
        for project_list in project_objects_list:
            project_lists.append(project_list)

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data = {
            'project_lists': project_lists,
            'current_page_no': page_obj.number,
            'next_page_number': next_page_number,
            'no_of_page': paginator.num_pages,
            'prev_page_number': prev_page_number
        }
        return JsonResponse(data)

    context = {
        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_projects': len(projects),
        'total_completed_projects': len(published_projects.filter(is_closed=True)),
        'page_obj': page_obj
    }
    print('ok')
    return render(request, 'projectapp/index.html', context)


@cache_page(60 * 15)
def project_list_View(request):
    """

    """
    project_list = Project.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(project_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'projectapp/project-list.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
@user_is_buyer
def create_project_View(request):
    """
    Provide the ability to create project post
    """
    form = ProjectForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)


    # user = get_object_or_404(user=request.user, id=request.user.id)
    project_categories = ProjectCategory.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You are successfully posted your project! Please wait for review.')
            return redirect(reverse("projectapp:single-project", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'project_categories': project_categories
    }
    return render(request, 'projectapp/post-project.html', context)


def single_project_view(request, id):
    """
    Provide the ability to view project details
    """
    if cache.get(id):
        project = cache.get(id)
    else:
        project = get_object_or_404(Project, id=id)
        cache.set(id,project , 60 * 15)
    related_project_list = project.tags.similar_objects()

    paginator = Paginator(related_project_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'project': project,
        'page_obj': page_obj,
        'total': len(related_project_list)

    }
    return render(request, 'projectapp/project-single.html', context)


def search_result_view(request):
    """
        User can search project with multiple fields
    """
    project_list = Project.objects.order_by('-timestamp')
    # Keywords
    if 'project_title_or_company_name' in request.GET:
        project_title_or_company_name = request.GET['project_title_or_company_name']

        if project_title_or_company_name:
            project_list = project_list.filter(title__icontains=project_title_or_company_name) | project_list.filter(
                company_name__icontains=project_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            project_list = project_list.filter(location__icontains=location)

    # Project Type
    if 'project_type' in request.GET:
        project_type = request.GET['project_type']
        if project_type:
            project_list = project_list.filter(project_type__iexact=project_type)

    
    paginator = Paginator(project_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'projectapp/result.html', context)


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# @login_required(login_url=reverse_lazy('account:login'))
@user_is_farmer
def apply_project_view(request, id):
    form = ProjectApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)

    applicant = Applicant.objects.filter(user=user, project=id)

    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(request, 'You have successfully applied for this project!')
                return HttpResponseRedirect(reverse("core:single-project", kwargs={'id': id}))
        else:
            return HttpResponseRedirect(reverse("core:single-project", kwargs={'id': id}))
    else:
        messages.error(request, 'You already applied for the Project!')
        return HttpResponseRedirect(reverse("core:single-project", kwargs={'id': id}))



# @login_required(login_url=reverse_lazy('account:login'))
@login_required
def dashboard_view(request):
    """
    """
    projects = []
    savedprojects = []
    appliedprojects = []
    total_applicants = {}
    if request.user.role == 'buyer':

        projects = Project.objects.filter(user=request.user.id)
        for project in projects:
            count = Applicant.objects.filter(project=project.id).count()
            total_applicants[project.id] = count

    if request.user.role == 'farmer':
        savedprojects = BookmarkProject.objects.filter(user=request.user.id)
        appliedprojects = Applicant.objects.filter(user=request.user.id)
    context = {

        'projects': projects,
        'savedprojects': savedprojects,
        'appliedprojects':appliedprojects,
        'total_applicants': total_applicants
    }

    return render(request, 'projectapp/project-dashboard.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
@user_is_buyer
def delete_project_view(request, id):

    project = get_object_or_404(Project, id=id, user=request.user.id)

    if project:

        project.delete()
        messages.success(request, 'Your Project Post was successfully deleted!')

    return redirect('projectapp:project-dashboard')


# @login_required(login_url=reverse_lazy('account:login'))
@user_is_buyer
def make_complete_project_view(request, id):
    project = get_object_or_404(Project, id=id, user=request.user.id)

    if project:
        try:
            project.is_closed = True
            project.save()
            messages.success(request, 'Your Project was marked closed!')
        except:
            messages.warning(request, 'Something went wrong !')
            
    return redirect('projectapp:project-dashboard')



# @login_required(login_url=reverse_lazy('account:login'))
@user_is_buyer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(project=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'projectapp/all-applicants.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
@user_is_farmer
def delete_bookmark_view(request, id):

    project = get_object_or_404(BookmarkProject, id=id, user=request.user.id)

    if project:

        project.delete()
        messages.success(request, 'Saved Project was successfully deleted!')

    return redirect('projectapp:dashboard')


# @login_required(login_url=reverse_lazy('account:login'))
@user_is_buyer
def applicant_details_view(request, id):

    applicant = get_object_or_404(user=request.user, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'projectapp/applicant-details.html', context)

# @login_required(login_url=reverse_lazy('account:login'))
@user_is_farmer
def project_bookmark_view(request, id):
    form = ProjectBookmarkForm(request.POST or None)

    user = request.user
    try:
        bookmark = BookmarkProject.objects.get(user=user, project=id)
    except BookmarkProject.DoesNotExist:
        bookmark = None

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()

            messages.success(request, 'You have successfully saved this project!')
            return HttpResponseRedirect(reverse("core:single-project", kwargs={'id': id}))
    else:
        if bookmark is None:
            messages.error(request, 'You already saved this project!')
    
    return HttpResponseRedirect(reverse("core:single-project", kwargs={'id': id}))


# @login_required(login_url=reverse_lazy('account:login'))
@user_is_buyer
def project_edit_view(request, id=id):
    """
    Handle Project Update

    """

    project = get_object_or_404(Project, id=id, user=request.user.id)
    categories = ProjectCategory.objects.all()
    form = ProjectEditForm(request.POST or None, instance=project)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Project Post Was Successfully Updated!')
        return redirect(reverse("projectapp:single-project", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'projectapp/project-edit.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Q
from django.views.generic import ListView
from blogs.models import Blog, BlogCategory, Bookmark, BlogCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

class Index(View):
    def get(self, request):
        latest_blogs = Blog.objects.filter(is_active=True, is_published=True)[:6]
        popular = Blog.objects.filter(is_active=True, is_published=True).order_by("-views")[:3]
        return render(request, "index.html", {"latest": latest_blogs, "popular": popular})

class Trendings(ListView):
    model = Blog
    template_name = 'trendings.html'
    context_object_name = 'blogs'
    paginate_by = 9

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).order_by("-views")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.get_paginate_by(self.object_list))
        page = self.request.GET.get("page")

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context["blogs"] = blogs
        return context

class Popular(ListView):
    model = Blog
    template_name = 'popular.html'
    context_object_name = 'blogs'
    paginate_by = 9

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).order_by("-views")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.get_paginate_by(self.object_list))
        page = self.request.GET.get("page")

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context["blogs"] = blogs
        return context

class Latest(ListView):
    model = Blog
    template_name = 'latest.html'
    context_object_name = 'blogs'
    paginate_by = 9

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).order_by("-published_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.get_paginate_by(self.object_list))
        page = self.request.GET.get("page")

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context["blogs"] = blogs
        return context

class Search(ListView):
    model = Blog
    template_name = "search.html"
    context_object_name = "blogs"
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get("query", "")
        blogs = Blog.objects.filter(
            (Q(title__icontains=query) | Q(desc__icontains=query)), is_active=True
        ).order_by("-views")
        return blogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.get_paginate_by(self.object_list))
        page = self.request.GET.get("page")

        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context["blogs"] = blogs
        context["query"] = self.request.GET.get("query")
        return context

class BlogCategoryView(View):
    def get(self, request):
        blogcategories = BlogCategory.objects.all()
        return render(request, "blogcategory.html", {"blogcategories": blogcategories})

class GetBlogCategory(View):
    def get(self, request, cat):
        blogcategory = get_object_or_404(BlogCategory.objects.filter(slug=cat, is_active=True))
        return render(request, "get_blogcategory.html", {"blogcategory": blogcategory})

class TermsAndConditions(View):
    def get(self, request):
        return render(request, "terms-and-conditions.html")

class BookmarkView(ListView):
    model = Bookmark
    template_name = 'bookmark.html'
    context_object_name = 'bookmarks'
    paginate_by = 9

    def get_queryset(self):
        if self.request.user.is_anonymous:
            messages.warning(requests.request, "Auth required")
            return redirect("accounts:login")
        return Bookmark.objects.filter(creator=self.request.user).order_by("-created_on")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.get_paginate_by(self.object_list))
        page = self.request.GET.get("page")

        try:
            bookmarks = paginator.page(page)
        except PageNotAnInteger:
            bookmarks = paginator.page(1)
        except EmptyPage:
            bookmarks = paginator.page(paginator.num_pages)

        context["bookmarks"] = bookmarks
        return context