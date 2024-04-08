from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    # path("signUp/", views.registerView,  name="signUp"),
    # path("signIn/", views.loginView, name="signIn"),
    # path("logout/", views.logoutView, name="logout"),
    # path("profile/edit/<int:id>", views.profile_edit, name="profile-edit"),
    path('profile/edit/<int:id>/', views.profile_edit, name='profile-edit'),

    path('farmer/register/', views.farmer_registration, name='farmer-registration'),
    path('buyer/register/', views.buyer_registration, name='buyer-registration'),
    # path('profile/edit/<int:id>/', views.employee_edit_profile, name='edit-profile'),
    path('login/', views.user_logIn, name='login'),
    path('logout/', views.user_logOut, name='logout'),

    

]