from django.urls import path
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


]