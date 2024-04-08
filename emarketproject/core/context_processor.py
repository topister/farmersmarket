from core.models import Product, Category, Farmer, Buyer, Expert,CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages
from django.db.models import Min, Max, Count
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    farmers = Farmer.objects.all()
    buyers  = Buyer.objects.all()
    experts = Expert.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))


    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            messages.warning(request, "You need to login before accessing your wishlist.")
            wishlist = 0
    else:
        wishlist = 0


  


    # address = Address.objects.get(user=request.user)
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories': categories,
        'address':address,
        'farmers':farmers,
        'buyers':buyers,
        'experts':experts,
        "min_max_price": min_max_price,
        'wishlist':wishlist,
        }