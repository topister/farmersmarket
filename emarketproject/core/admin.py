from django.contrib import admin
from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'featured', 'product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_category']

class FarmerAdmin(admin.ModelAdmin):
    list_display = ['title', 'farmer_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'item', 'image', 'quantity', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartItems, CartItemsAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Address, AddressAdmin)
