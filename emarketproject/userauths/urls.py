from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("signUp/", views.registerView,  name="signUp"),
    path("signIn/", views.loginView, name="signIn"),
    path("logout/", views.logoutView, name="logout"),
    path("profile/edit/", views.profile_edit, name="profile-edit"),

    # path('login/',views.loginUser,name='login'),
    # path('logout/',views.logoutUser,name='logout'),
    # path('register/', views.registerUser, name='register'),  
    # path('update_profile/', views.update_profile, name='update_profile'),  
    # # path('profile/<uuid:profile_id>/',views.profile_detail, name='profile_detail'),
    # path('user/profile/<int:profile_id>/', views.profile_detail, name='profile_detail'),

    # path('coursebase/', views.coursebase, name='coursebase'),

]