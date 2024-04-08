from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from blogs.models import BlogCategory, Blog, Comment
from django.utils import timezone
from .forms import CKEditorForm

# Create your views here.
class ManageBlog(View):
    def get(self, request):
        blogs = Blog.objects.filter(is_active=True, creator=request.user)
        return render(request, "management/blog.html", {"blogs": blogs})

class ManageBlogCategory(View):
    def get(self, request):
        blogcategories = BlogCategory.objects.filter(is_active=True)
        return render(request, "management/blogcategory.html", {"blogcategories": blogcategories})


class CreateBlog(View):
    def get(self, request):
        form = CKEditorForm()
        blogcategories = BlogCategory.objects.filter(is_active=True)
        return render(request, "management/create_blog.html", {"form": form, "blogcategories": blogcategories})

    def post(self, request):
        data = request.POST
        title = data.get("title")
        desc = data.get("desc")
        content = data.get("content")
        thumbnail = request.FILES.get("thumbnail")
        blogcategories = data.getlist("blogcategories") 
        status = data.get("status")

        if not (title and desc and content and thumbnail and blogcategories and status):
            messages.info(request, "title, desc, content, thumbnail, blogcategories, or status can't be empty")
            return redirect("manage:create_blog")

        try:
            status = bool(int(status))
        except:
            messages.info(request, "Something wrong with status")
            return redirect("manage:create_blog")

        blog = Blog(
            title = title,
            desc = desc,
            content = content,
            creator = request.user,
            thumbnail = thumbnail,
            is_published = status
        )
        blog.save()
        for id in blogcategories:
            try:
                c = BlogCategory.objects.get(id=int(id))
                blog.blogcategories.add(c)
            except Exception as e:
                pass

        blog.save()
        messages.success(request, "Blog created")

        return redirect("manage:create_blog")


class CreateBlogCategory(View):
    def get(self, request):
        return render(request, "management/create_blogcategory.html")

    def post(self, request):
        data = request.POST
        blogcategory = data.get("blogcategory")
        desc = data.get("desc")

        c = BlogCategory.objects.filter(blogcategory=blogcategory).first()
        if c is not None:
            messages.warning(request, "Blog Category already exists")
        else:
            c = BlogCategory(
                blogcategory=blogcategory,
                desc=desc
            )
            c.save()
            messages.success(request, "Blog Category created")
        return redirect("manage:create_blogcategory")
        
class EditBlog(View):
    def get(self, request, id):
        blog = Blog.objects.filter(id=id, creator=request.user).first()
        if blog is None:
            messages.info(request, "Blog not exists")
            return redirect("manage:blog")
        blogcategories = BlogCategory.objects.all()
        form = CKEditorForm({"content": blog.content})
        return render(request, "management/edit_blog.html", {"blog": blog, "blogcategories": blogcategories, "form": form})
    
    def post(self, request, id = None):
        data = request.POST
        id = data.get("id")
        blog = Blog.objects.filter(is_active=True, creator=request.user, id=id).first()
        if blog is None:
            messages.info(request, "Blog doesn't exists")
            return redirect("manage:blog")

        title = data.get("title")
        desc = data.get("desc")
        content = data.get("content")
        status = data.get("status")
        thumbnail = request.FILES.get("thumbnail")
        blogcategories = data.getlist("blogcategories")

        blog.title = title
        blog.desc = desc
        blog.content = content
        if thumbnail:
            blog.thumbnail = thumbnail

        try:
            status = int(status)
            if not blog.is_published and status:
                blog.published_on = timezone.now()
            blog.is_published = bool(status)
        except:
            messages.info(request, "Error while updating status")
        
        blog.blogcategories.set([])
        for id in blogcategories:
            try:
                c = BlogCategory.objects.get(id=int(id))
                blog.blogcategories.add(c)
            except Exception as e:
                pass

        blog.save()
        messages.success(request, "Changes saved")

        return redirect("manage:blog")

class DeleteBlog(View):
    def get(self, request, id):
        blog = Blog.objects.filter(id=id, creator=request.user).first()
        if blog is None:
            messages.warning(request, "Blog doesn't exists")
        else:
            blog.is_active = False
            blog.save()
            messages.info(request, "Blog deleted")

        return redirect("manage:blog")

class EditBlogCategory(View):
    def get(self, request, id):
        blogcategory = get_object_or_404(BlogCategory, id=id, is_active=True)
        return render(request, "management/edit_blogcategory.html", {"blogcategory": blogcategory})

    def post(self, request, id):
        c = BlogCategory.objects.filter(id=id, is_active=True).first()
        data = request.POST
        blogcategory, desc = data.get("blogcategory"), data.get("desc")
        if not ((blogcategory and desc) or c):
            messages.warning(request, "Blog Category or Desc can't be empty. OR Blog Category doesn't exists")
            return redirect("manage:blogcategory")
        c.blogcategory = blogcategory
        c.desc = desc
        c.save()
        messages.success(request, "Changes saved")
        return redirect("manage:blogcategory")
        

class DeleteBlogCategory(View):
    def get(self, request, id):
        blogcategory = get_object_or_404(BlogCategory, id=id)
        blogcategory.is_active = False
        blogcategory.save()
        messages.info(request, "Blog Category removed")
        return redirect("manage:blogcategory")

class ManageComment(View):
    def get(self, request):
        comments = Comment.objects.filter(is_active=True, blog__in=Blog.objects.filter(creator=request.user))
        return render(request, "management/comment.html", {"comments": comments})

class DeleteComment(View):
    def get(self, request, id):
        comment = get_object_or_404(Comment.objects.filter(id=id, is_active=True))
        if comment.blog.creator.username != request.user.username:
            messages.warning(request, "You are not author of that blog")
            return redirect("manage:comment")
        comment.is_active = False
        comment.save()
        messages.success(request, "Comment deleted")
        return redirect("manage:comment")