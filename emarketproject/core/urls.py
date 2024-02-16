from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),

    # products

    path('products/', views.product_list, name="product-list"),

    # categories
    path('categories/', views.category_list, name="category-list"),
    path('categories/<categoryId>/', views.product_list_category, name="product-list-category"),

    # farmers
    path('farmers/', views.farmer_list, name='farmer-list'),


]