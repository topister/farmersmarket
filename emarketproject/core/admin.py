from django.contrib import admin

from core.models import Applicant, BookmarkProject, Project, Product, Category, Farmer, Buyer,Expert, CartOrder, CartItems, ProjectCategory, Wishlist, Address, ProductReview, ProductImages, ContactUs

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'farmer', 'featured', 'product_status', 'productId']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_category']

class FarmerAdmin(admin.ModelAdmin):
    list_display = ['title', 'farmer_image']


class BuyerAdmin(admin.ModelAdmin):
    list_display = ['title', 'buyer_image']

class ExpertAdmin(admin.ModelAdmin):
    list_display = ['title', 'expert_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['product_status', 'paid_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']


class CartItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_number', 'item', 'image', 'quantity', 'price', 'total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']
    list_editable = ['address', 'status']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'subject']

admin.site.register(ProjectCategory)

class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('project','user','timestamp')
    
admin.site.register(Applicant,ApplicantAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_closed','timestamp')

admin.site.register(Project,ProjectAdmin)

class BookmarkProjectAdmin(admin.ModelAdmin):
    list_display = ('project','user','timestamp')

admin.site.register(BookmarkProject,BookmarkProjectAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartItems, CartItemsAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ContactUs, ContactUsAdmin)


