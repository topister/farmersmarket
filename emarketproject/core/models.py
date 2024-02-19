from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe
from userauths.models import User
import uuid
from taggit.managers import TaggableManager


STATUS_CHOICE=(
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS=(
    ("draft", "Draft"),
    ("disabled", "disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In review"),
    ("published", "Published"),
)
RATING=(
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

def user_directory_path(instance, filename):
    

    return 'user_{0}/{1}'.format(instance.user.id, filename)

class CustomUUIDField(models.UUIDField):
    def __init__(self, length=10, prefix="CAT", alphabet="12345abcdefghi", *args, **kwargs):
        self.length = length
        self.prefix = prefix
        self.alphabet = alphabet
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        # Convert the UUID to a string and remove hyphens
        value_str = str(value).replace("-", "")

        # Adjust the length by truncating or padding with zeros
        if len(value_str) > self.length:
            value_str = value_str[:self.length]
        elif len(value_str) < self.length:
            value_str = value_str + "0" * (self.length - len(value_str))

        # Combine the prefix and adjusted UUID
        final_value = self.prefix + value_str

        return uuid.UUID(final_value)
    

# Create your models here.
class Category(models.Model):
    # categoryId = CustomUUIDField(unique=True, length=10, max_length=20, prefix="CAT", alphabet="12345abcdefghi")

    categoryId = ShortUUIDField(unique=True, length=10, max_length=20, prefix="CAT", alphabet="12345abcdefghi")

    title = models.CharField(max_length=100, default="Food stuff")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def image_category(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass

class Farmer(models.Model):
    farmerId = ShortUUIDField(unique=True, length=10, max_length=20, prefix="farm", alphabet="12345abcdefghi")
    title = models.CharField(max_length=100, default="Digify farmer")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    image = models.ImageField(upload_to=user_directory_path, default="farmer.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="farmer.jpg")
    description = models.TextField(null=True, blank=True, default="I am a great farmer")
    address = models.CharField(max_length=100, default="Busia, Kenya")
    contact = models.CharField(max_length=100, default="+254740298531")
    chat_response_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="98")
    days_return = models.CharField(max_length=100, default="7")
    warranty_period = models.CharField(max_length=100, default="4")
    # Whenever the farmer is deleted his/her shop is not deleted
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name_plural = "Farmers"

    def farmer_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    productId = ShortUUIDField(unique=True, length=10, max_length=20, prefix="prd", alphabet="12345abcdefghi")
    title = models.CharField(max_length=100, default="Fresh vegetables")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    description = models.TextField(null=True, blank=True, default="This is product")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    farmer = models.ForeignKey(Farmer, on_delete=models.SET_NULL, null=True, related_name="farmer")

    price = models.DecimalField(max_digits=999999999, decimal_places=2, default=9.99)
    old_price = models.DecimalField(max_digits=999999999, decimal_places=2, default=19.99)
 
    specification = models.TextField(null=True, blank=True, default="Specifications")
    type = models.CharField(max_length=100, default="Organic product", null=True, blank=True)
    stock_count = models.CharField(max_length=100, default="5", null=True, blank=True)


    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    tags = TaggableManager(blank=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=5, max_length=10, prefix="sku", alphabet="0123456789")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    def get_discount_percentage(self):
        new_price =  float(self.old_price - self.price) / float(self.old_price) * 100
        return new_price
    

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

# cart, order, order items 
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, default=9.99)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=40, default="processing")
    
    class Meta:
        verbose_name_plural = "Cart Order"




class CartItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, default=9.99)

    total = models.DecimalField(max_digits=999999999, decimal_places=2, default=9.99)

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50"/>' % (self.image))
    
# product review, wishlist, address
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name_plural = "Product Reviews"

    
    def __str__(self):
        return self.product.title
    
    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)



    class Meta:
        verbose_name_plural = "Wishlist"

    
    def __str__(self):
        return self.product.title
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=150, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"

   
