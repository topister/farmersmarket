from core.models import Product, Category, Farmer, CartOrder, CartItems, Wishlist, Address, ProductReview, ProductImages


def default(request):
    categories = Category.objects.all()
    farmers = Farmer.objects.all()

    # address = Address.objects.get(user=request.user)
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {
        'categories': categories,
        'address':address,
        'farmers':farmers,
        }