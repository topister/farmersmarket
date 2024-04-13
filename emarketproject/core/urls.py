from django.urls import include, path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path("ckeditor/", include("ckeditor_uploader.urls")), #For CKEditor5

    path("management/", include("management.urls")),

    # path("index/", views.Index.as_view(), name="index"),
    path("trendings/", views.Trendings.as_view(), name="trendings"),
    path("latest/", views.Latest.as_view(), name="latest"),
    path("popular/", views.Popular.as_view(), name="popular"),
    path("searchblog/", views.SearchBlog.as_view(), name="searchblog"),
    path("bookmark/", views.BookmarkView.as_view(), name="bookmark"),
    path("terms-and-conditions/", views.TermsAndConditions.as_view(), name="terms_and_conditions"),
    path("blogcategory/", views.BlogCategoryView.as_view(), name="blogcategory"),
    path("blogcategory/<slug:cat>/", views.GetBlogCategory.as_view(), name="get_blogcategory"),

    # products

    path('products/', views.product_list, name="product-list"),
    path('products/<productId>', views.product_detail, name="product-detail"),

    # categories
    path('categories/', views.category_list, name="category-list"),
    path('categories/<categoryId>/', views.product_list_category, name="product-list-category"),

    # farmers
    path('farmers/', views.farmer_list, name='farmer-list'),
    path('farmer/<farmerId>', views.farmer_details, name= "farmer-detail" ),

    # buyers
    path('buyers/', views.buyer_list, name='buyer-list'),
    path('buyer/<buyerId>', views.buyer_details, name= "buyer-detail" ),

    # experts
    path('experts/', views.expert_list, name='expert-list'),
    path('expert/<expertId>', views.expert_details, name= "expert-detail" ),


    # tags
    path("products/tags/<slug:tag_slug>/",views.tag_list , name="tag-list"),

    # add reviews
    path('ajax-add-review/<productId>/', views.ajax_add_review, name='ajax-add-review'),

    # Search
    path('searchproduct/', views.search, name='searchproduct'),

    # Filter products listings
    path('filter-products/', views.filter_products_listing, name='filter-products'),

    # Add to cart
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),


    # Add to cart homepage url
    path('cart/', views.cart_view_homepage, name="cart"),

    # Delete cart item
    path('delete-cart-item/', views.delete_cart_item, name="delete-cart-item"),

    # Update cart item
    path('update-cart/', views.update_cart, name="update-cart"),

    # checkout
    path('checkout/', views.checkout, name='checkout'),

    # paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    # paypal payment successful
    # path('paypal-success/', views.paypal_successful, name='paypal-success'),
    
    # paypal payment failed
    path('payment-failed/', views.payment_failed, name='payment-failed'),

    # payment completed vie
    path('payment-completed/', views.payment_completed_view, name='payment-completed'),

    # General dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # buyer dashboard
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer-dashboard'),

    # seller dashboard
    path('seller-dashboard/', views.seller_dashboard, name='seller-dashboard'),

    # view ordered details
    path('dashboard/order-detail/<int:id>', views.view_order_detail, name='order-detail'),

    # make address defualt
    path('default_address/', views.default_address, name='default_address'),

    # wishlist view
    path('wishlist/',views.wishlist, name='wishlist'),

    path('add-to-wishlist/',views.add_to_wishlist, name='add-to-wishlist'),


    # Removing products from wishlist
    path('wishlist-remove/',views.wishlist_remove, name='wishlist-remove'),

    # Contact  us page
    path('contact/', views.contact, name="contact"),
    path('ajax-contact-form/', views.contact_ajax, name="ajax-contact-form"),

    # About us page
    path("about-us/", views.about_us, name="about-us"),
    path("purchase_guide/", views.purchase_guide, name="purchase_guide"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_of_service/", views.terms_of_service, name="terms_of_service"),


    # Project part
    path('projects/', views.project_list_View, name='project-list'),
    path('project/create/', views.create_project_View, name='create-project'),
    path('project/<int:id>/', views.single_project_view, name='single-project'),
    path('apply-project/<int:id>/', views.apply_project_view, name='apply-project'),
    path('bookmark-project/<int:id>/', views.project_bookmark_view, name='bookmark-project'),
    path('result/', views.search_result_view, name='search_result'),
    path('project-dashboard/', views.dashboard_view, name='project-dashboard'),
    path('project-dashboard/buyer/project/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('project-dashboard/buyer/project/edit/<int:id>', views.project_edit_view, name='edit-project'),
    path('project-dashboard/buyer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('project-dashboard/buyer/close/<int:id>/', views.make_complete_project_view, name='complete'),
    path('project-dashboard/buyer/delete/<int:id>/', views.delete_project_view, name='delete'),
    path('project-dashboard/farmer/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),




]