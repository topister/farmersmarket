from django.urls import include, path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),

    # products

    path('products/', views.product_list, name="product-list"),
    path('products/<productId>', views.product_detail, name="product-detail"),

    # categories
    path('categories/', views.category_list, name="category-list"),
    path('categories/<categoryId>/', views.product_list_category, name="product-list-category"),

    # farmers
    path('farmers/', views.farmer_list, name='farmer-list'),
    path('farmer/<farmerId>', views.farmer_details, name= "farmer-detail" ),

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
    path('dashboard/order-detail/<int:id>', views.view_order_detail, name="order-detail"),







]