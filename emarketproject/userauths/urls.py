from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns = [
    path("signUp/", views.registerView,  name="signUp"),
    path("signIn/", views.loginView, name="signIn"),
    path("logout/", views.logoutView, name="logout"),
    path("profile/edit/", views.profile_edit, name="profile-edit")

]