from ast import Module
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
import requests
from core.models import Applicant, BookmarkJob, Job, Product, Category,ProjectCategory, Farmer, Expert, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages, ContactUs
from django.http import JsonResponse
from core.permission import user_is_employee, user_is_employer
from userauths.models import Profile
from taggit.models import Tag
from django.db.models import Count, Avg
from core.forms import JobApplyForm, JobBookmarkForm, JobEditForm, JobForm, ProductReviewForm
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

def expert_details(request, expertId):
    experts = Expert.objects.get(expertId=expertId)
    # products = Product.objects.filter(farmer=farmers, product_status="published")
    context = {
        "experts": experts,
        
    }

    return render(request, "core/expert-detail.html", context)

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
# from jobapp.forms import *
# from jobapp.models import *
# from jobapp.permission import *
# User = get_user_model()

# from django.http import HttpRequest

# def home_view(request):

#     published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
#     jobs = published_jobs.filter(is_closed=False)
#     # total_candidates = request.user.objects.filter(role='employee').count()
#     total_candidates = User.objects.filter(role='employee').count()
#     total_companies = User.objects.filter(role='employer').count()
#     # total_companies = request.user.objects.filter(role='employer').count()
#     paginator = Paginator(jobs, 3)
#     page_number = request.GET.get('page',None)
#     page_obj = paginator.get_page(page_number)

#     if request.is_ajax():
#         job_lists=[]
#         job_objects_list = page_obj.object_list.values()
#         for job_list in job_objects_list:
#             job_lists.append(job_list)
        

#         next_page_number = None
#         if page_obj.has_next():
#             next_page_number = page_obj.next_page_number()

#         prev_page_number = None       
#         if page_obj.has_previous():
#             prev_page_number = page_obj.previous_page_number()

#         data={
#             'job_lists':job_lists,
#             'current_page_no':page_obj.number,
#             'next_page_number':next_page_number,
#             'no_of_page':paginator.num_pages,
#             'prev_page_number':prev_page_number
#         }    
#         return JsonResponse(data)
    
#     context = {

#     'total_candidates': total_candidates,
#     'total_companies': total_companies,
#     'total_jobs': len(jobs),
#     'total_completed_jobs':len(published_jobs.filter(is_closed=True)),
#     'page_obj': page_obj
#     }
#     print('ok')
#     return render(request, 'jobapp/index.html', context)

from django.http import HttpRequest, JsonResponse

def home_view(request):

    published_jobs = Job.objects.filter(is_published=True).order_by('-timestamp')
    jobs = published_jobs.filter(is_closed=False)
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()
    paginator = Paginator(jobs, 3)
    page_number = request.GET.get('page', None)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        job_lists = []
        job_objects_list = page_obj.object_list.values()
        for job_list in job_objects_list:
            job_lists.append(job_list)

        next_page_number = None
        if page_obj.has_next():
            next_page_number = page_obj.next_page_number()

        prev_page_number = None
        if page_obj.has_previous():
            prev_page_number = page_obj.previous_page_number()

        data = {
            'job_lists': job_lists,
            'current_page_no': page_obj.number,
            'next_page_number': next_page_number,
            'no_of_page': paginator.num_pages,
            'prev_page_number': prev_page_number
        }
        return JsonResponse(data)

    context = {
        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_jobs': len(jobs),
        'total_completed_jobs': len(published_jobs.filter(is_closed=True)),
        'page_obj': page_obj
    }
    print('ok')
    return render(request, 'jobapp/index.html', context)


@cache_page(60 * 15)
def job_list_View(request):
    """

    """
    job_list = Job.objects.filter(is_published=True,is_closed=False).order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employer
def create_job_View(request):
    """
    Provide the ability to create job post
    """
    form = JobForm(request.POST or None)

    user = get_object_or_404(user=request.user, id=request.user.id)
    categories = ProjectCategory.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()
            messages.success(
                    request, 'You are successfully posted your job! Please wait for review.')
            return redirect(reverse("jobapp:single-job", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)


def single_job_view(request, id):
    """
    Provide the ability to view job details
    """
    if cache.get(id):
        job = cache.get(id)
    else:
        job = get_object_or_404(Job, id=id)
        cache.set(id,job , 60 * 15)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)


def search_result_view(request):
    """
        User can search job with multiple fields

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    # job_title_or_company_name = request.GET.get('text')
    # location = request.GET.get('location')
    # job_type = request.GET.get('type')

    #     job_list = Job.objects.all()
    #     job_list = job_list.filter(
    #         Q(job_type__iexact=job_type) |
    #         Q(title__icontains=job_title_or_company_name) |
    #         Q(location__icontains=location)
    #     ).distinct()

    # job_list = Job.objects.filter(job_type__iexact=job_type) | Job.objects.filter(
    #     location__icontains=location) | Job.objects.filter(title__icontains=text) | Job.objects.filter(company_name__icontains=text)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employee
# def apply_job_view(request, id):

#     form = JobApplyForm(request.POST or None)

#     user = get_object_or_404(user=request.user, id=request.user.id)
#     applicant = Applicant.objects.filter(user=user, job=id)

#     if not applicant:
#         if request.method == 'POST':

#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.user = user
#                 instance.save()

#                 messages.success(
#                     request, 'You have successfully applied for this job!')
#                 return redirect(reverse("jobapp:single-job", kwargs={
#                     'id': id
#                 }))

#         else:
#             return redirect(reverse("jobapp:single-job", kwargs={
#                 'id': id
#             }))

#     else:

#         messages.error(request, 'You already applied for the Job!')

#         return redirect(reverse("jobapp:single-job", kwargs={
#             'id': id
#         }))

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employee
def apply_job_view(request, id):
    form = JobApplyForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)

    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(request, 'You have successfully applied for this job!')
                return HttpResponseRedirect(reverse("core:single-job", kwargs={'id': id}))
        else:
            return HttpResponseRedirect(reverse("core:single-job", kwargs={'id': id}))
    else:
        messages.error(request, 'You already applied for the Job!')
        return HttpResponseRedirect(reverse("core:single-job", kwargs={'id': id}))



@login_required(login_url=reverse_lazy('account:login'))
def dashboard_view(request):
    """
    """
    jobs = []
    savedjobs = []
    appliedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
        appliedjobs = Applicant.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'appliedjobs':appliedjobs,
        'total_applicants': total_applicants
    }

    return render(request, 'jobapp/project-dashboard.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employer
def make_complete_job_view(request, id):
    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:
        try:
            job.is_closed = True
            job.save()
            messages.success(request, 'Your Job was marked closed!')
        except:
            messages.success(request, 'Something went wrong !')
            
    return redirect('jobapp:project-dashboard')



# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(job=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(user=request.user, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'jobapp/applicant-details.html', context)


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employee
# def job_bookmark_view(request, id):

#     form = JobBookmarkForm(request.POST or None)

#     user = get_object_or_404(user=request.user, id=request.user.id)
#     applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

#     if not applicant:
#         if request.method == 'POST':

#             if form.is_valid():
#                 instance = form.save(commit=False)
#                 instance.user = user
#                 instance.save()

#                 messages.success(
#                     request, 'You have successfully save this job!')
#                 return redirect(reverse("jobapp:single-job", kwargs={
#                     'id': id
#                 }))

#         else:
#             return redirect(reverse("jobapp:single-job", kwargs={
#                 'id': id
#             }))

#     else:
#         messages.error(request, 'You already saved this Job!')

#         return redirect(reverse("jobapp:single-job", kwargs={
#             'id': id
#         }))

# from django.shortcuts import get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.urls import reverse
# from django.http import HttpResponseRedirect
# from django.contrib import messages

# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employee
# def job_bookmark_view(request, id):
#     form = JobBookmarkForm(request.POST or None)

#     user = get_object_or_404(User, id=request.user.id)
#     bookmark = get_object_or_404(BookmarkJob, user=user, job=id)

#     if request.method == 'POST':
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = user
#             instance.save()

#             messages.success(request, 'You have successfully saved this job!')
#             return HttpResponseRedirect(reverse("jobapp:single-job", kwargs={'id': id}))
#     else:
#         messages.error(request, 'You already saved this job!')
    
#     return HttpResponseRedirect(reverse("jobapp:single-job", kwargs={'id': id}))

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employee
def job_bookmark_view(request, id):
    form = JobBookmarkForm(request.POST or None)

    user = request.user
    try:
        bookmark = BookmarkJob.objects.get(user=user, job=id)
    except BookmarkJob.DoesNotExist:
        bookmark = None

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()

            messages.success(request, 'You have successfully saved this job!')
            return HttpResponseRedirect(reverse("core:single-job", kwargs={'id': id}))
    else:
        if bookmark is None:
            messages.error(request, 'You already saved this job!')
    
    return HttpResponseRedirect(reverse("core:single-job", kwargs={'id': id}))


# @login_required(login_url=reverse_lazy('account:login'))
# @user_is_employer
def job_edit_view(request, id=id):
    """
    Handle Job Update

    """

    job = get_object_or_404(Job, id=id, user=request.user.id)
    categories = ProjectCategory.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)