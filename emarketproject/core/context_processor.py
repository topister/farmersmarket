from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages
from django.db.models import Min, Max


def default(request):
    categories = Category.objects.all()
    farmers = Farmer.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))


    # address = Address.objects.get(user=request.user)
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories': categories,
        'address':address,
        'farmers':farmers,
        "min_max_price": min_max_price,
        }