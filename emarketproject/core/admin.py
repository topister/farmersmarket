from django.contrib import admin

from core.models import Applicant, BookmarkJob, Job, Product, Category, Farmer, Expert, CartOrder, CartItems, ProjectCategory, Wishlist, Address, ProductReview, ProductImages, ContactUs

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
    list_display = ('job','user','timestamp')
    
admin.site.register(Applicant,ApplicantAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = ('title','is_published','is_closed','timestamp')

admin.site.register(Job,JobAdmin)

class BookmarkJobAdmin(admin.ModelAdmin):
    list_display = ('job','user','timestamp')

admin.site.register(BookmarkJob,BookmarkJobAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Expert, ExpertAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartItems, CartItemsAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ContactUs, ContactUsAdmin)


# Trying project part
# from django.contrib import admin
# from .models import Course, Module, Video, Comment, SubComment, Notes, Monitor, UserProgress, CourseProgress, Quiz, Question, Answer, Enrollment

# Register your models here.

# admin.site.register(Course)
# admin.site.register(Module)
# admin.site.register(Video)
# admin.site.register(Comment)
# admin.site.register(SubComment)
# admin.site.register(Notes)
# admin.site.register(Monitor)
# admin.site.register(UserProgress)
# admin.site.register(CourseProgress)
# admin.site.register(Quiz)
# admin.site.register(Question)
# admin.site.register(Answer)
# admin.site.register(Enrollment)



