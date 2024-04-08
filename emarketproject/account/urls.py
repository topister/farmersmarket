from django.urls import path
from account import views

app_name = "account"

urlpatterns = [

    path('farmer/register/', views.farmer_registration, name='farmer-registration'),
    path('buyer/register/', views.buyer_registration, name='buyer-registration'),
    path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),
]