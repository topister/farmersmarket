from django.urls import path
from . import views

app_name = "management"

urlpatterns = [
    path("blog/", views.ManageBlog.as_view(), name="blog"),
    path("blogcategory/", views.ManageBlogCategory.as_view(), name="blogcategory"),
    path("comment/", views.ManageComment.as_view(), name="comment"),

    path("create/blog/", views.CreateBlog.as_view(), name="create_blog"),
    path("create/blogcategory/", views.CreateBlogCategory.as_view(), name="create_blogcategory"),

    path("delete/blog/<int:id>/", views.DeleteBlog.as_view(), name="delete_blog"),
    path("delete/blogcategory/<int:id>", views.DeleteBlogCategory.as_view(), name="delete_blogcategory"),
    path("delete/comment/<int:id>", views.DeleteComment.as_view(), name="delete_comment"),

    path("edit/blog/<int:id>/", views.EditBlog.as_view(), name="edit_blog"),
    path("edit/blogcategory/<int:id>", views.EditBlogCategory.as_view(), name="edit_blogcategory"),
]