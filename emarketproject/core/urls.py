from django.urls import include, path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path("ckeditor/", include("ckeditor_uploader.urls")), #For CKEditor5

    # products

    path('products/', views.product_list, name="product-list"),
    path('products/<productId>', views.product_detail, name="product-detail"),

    # categories
    path('categories/', views.category_list, name="category-list"),
    path('categories/<categoryId>/', views.product_list_category, name="product-list-category"),

    # farmers
    path('farmers/', views.farmer_list, name='farmer-list'),
    path('farmer/<farmerId>', views.farmer_details, name= "farmer-detail" ),

    # experts
    path('experts/', views.expert_list, name='expert-list'),
    path('expert/<expertId>', views.expert_details, name= "expert-detail" ),


    # tags
    path("products/tags/<slug:tag_slug>/",views.tag_list , name="tag-list"),

    # add reviews
    path('ajax-add-review/<productId>/', views.ajax_add_review, name='ajax-add-review'),

    # Search
    path('search/', views.search, name='search'),

    # Filter products listings
    path('filter-products/', views.filter_products_listing, name='filter-products'),

    # Add to cart
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),


    # Add to cart homepage url
    path('cart/', views.cart_view_homepage, name="cart"),

    # Delete cart item
    path('delete-cart-item/', views.delete_cart_item, name="delete-cart-item"),

    # Update cart item
    path('update-cart/', views.update_cart, name="update-cart"),

    # checkout
    path('checkout/', views.checkout, name='checkout'),

    # paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    # paypal payment successful
    path('paypal-success/', views.paypal_successful, name='paypal-success'),
    
    # paypal payment failed
    path('paypal-fail/', views.paypal_failed, name='paypal-fail'),

    # General dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # buyer dashboard
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer-dashboard'),

    # seller dashboard
    path('seller-dashboard/', views.seller_dashboard, name='seller-dashboard'),

    # view ordered details
    path('dashboard/order-detail/<int:id>', views.view_order_detail, name='order-detail'),

    # make address defualt
    path('default_address/', views.default_address, name='default_address'),

    # wishlist
    # path('wishlist/', views.wishlist, name="wishlist"),

    # add to wishlist
    # path('add-wishlist/', views.add_wishlist, name="add-wishlist"),

    # wishlist view
    path('wishlist/',views.wishlist, name='wishlist'),

    path('add-to-wishlist/',views.add_to_wishlist, name='add-to-wishlist'),


    # Removing products from wishlist
    path('wishlist-remove/',views.wishlist_remove, name='wishlist-remove'),

    # Contact  us page
    path('contact/', views.contact, name="contact"),
    path('ajax-contact-form/', views.contact_ajax, name="ajax-contact-form"),

    # About us page
    path("about-us/", views.about_us, name="about-us"),
    path("purchase_guide/", views.purchase_guide, name="purchase_guide"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_of_service/", views.terms_of_service, name="terms_of_service"),


    # Project part
    path('projects/', views.home_view, name='home'),
    path('jobs/', views.job_list_View, name='job-list'),
    path('job/create/', views.create_job_View, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('about/', views.single_job_view, name='about'),
    path('contact/', views.single_job_view, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('project-dashboard/', views.dashboard_view, name='project-dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/close/<int:id>/', views.make_complete_job_view, name='complete'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),




]