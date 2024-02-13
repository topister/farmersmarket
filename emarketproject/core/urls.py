from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('products/', views.product_list, name="product-list"),
    path('categories/', views.category_list, name="category-list"),
    path('categories/<categoryId>/', views.product_list_category, name="product-list-category"),

]