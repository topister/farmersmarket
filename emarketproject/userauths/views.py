from django.http import HttpResponse
from django.shortcuts import redirect, render
from userauths.forms import SignUpForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User, Profile
from django.contrib.auth import get_user_model
User = get_user_model()

# User = settings.AUTH_USER_MODEL

# Create your views here.
def registerView(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,  f"Account created for {username}! Is now able to log in.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            
            login(request, new_user)

            return redirect("core:index")
        
        
    else:
        
        form = SignUpForm()

    

    context = {
        'form': form,
    }
    return render(request, "userauths/signUp.html", context)

def loginView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"You are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged in as {user.username}")
                return redirect("core:index")
            
            else:
                messages.warning(request, "User does not exist. Create new account!")


        except:
            messages.warning(request, f"User with  the email address {email} does not exist.")

        
    context = {

    }
        
    return render(request, "userauths/signIn.html", context)

def logoutView(request):
    logout(request)
    messages.success(request, "You logged out")

    return redirect("userauths:signIn")


# def profile_edit(request):
#     profile = Profile.objects.get(user=request.user)
#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=profile) 
#         if form.is_valid():
#             profile_save = form.save(commit=False)
#             profile_save.user = request.user
#             profile_save.save()
#             messages.success(request, "Profile updated successfully!")
#             return redirect('core:dashboard')
#     else:
#         form = ProfileForm(instance=profile)
#     context = {
#          'form':form,
#          'profile':profile,
#      }
#     return render(request, 'userauths/profile_edit.html', context)



from django.contrib.auth.decorators import login_required

@login_required
def profile_edit(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Handle the case where the profile does not exist for the user
        # You might want to create a new profile or redirect to a profile creation page
        return HttpResponse("Profile does not exist for this user.")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile) 
        if form.is_valid():
            profile_save = form.save(commit=False)
            profile_save.user = request.user
            profile_save.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('core:dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
         'form': form,
         'profile': profile,
    }
    return render(request, 'userauths/profile_edit.html', context)


# Projects Part

# from django.http import HttpResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from .models import ProfileProject
# from django.contrib import messages
# from .models import Teacher, Student, Organization


# def coursebase(request):
#     return render(request, 'main/course_base.html')


# # messages.error(request,'User not found')
# # @login_required(login_url='login')

# def loginUser(request):
#     page = 'login'
#     if request.user.is_authenticated:
#         return redirect('index')

#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']

#         try:
#             user = User.objects.get(username=email)
#         except:
#             messages.error(request,'User not found')
#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             messages.error(request,'Username or password is incorrect')
#     return render(request,'user/login.html',)

# def logoutUser(request):
#     logout(request)
#     return redirect('index')

# def registerUser(request):
#     page='signup'
#     if (request.user.is_authenticated):
#         return redirect('index')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('name')
#             email = request.POST.get('email')
#             phone = request.POST.get('phone')
#             pwd = request.POST.get('password')
#             cnfrm_pwd = request.POST.get('confirmpassword')
#             try:
#                 if pwd == cnfrm_pwd:
#                     profile=ProfileProject.objects.filter(email=email)
#                     user=User.objects.filter(email=email)

#                     if not user.exists():
#                         user=User.objects.create_user(username=email,email=email)
#                         user.set_password(pwd)
#                         profile=ProfileProject.objects.create(user=user,name=username,email=email,phone=phone)
#                         student=Student.objects.create(profile=profile)
#                         user.save()
#                         profile.save()
#                         student.save()
#                         login(request, user)
#                         return redirect('index')
#                     else:
#                         return render(request, 'user/register.html',{"msg": "User already exists"})
#                 else:
#                     return render(request, 'user/register.html',{ "msg":"Confirm Password is not equal to Password" }) 
                   
#             except Exception as e:
#                 return HttpResponse(e)
#         return render(request, 'user/register.html')        


# def update_profile(request):
#     print(request.user)
#     if request.user.is_authenticated:

#         try:
#             r_profile = ProfileProject.objects.get(user=request.user)
#         except ProfileProject.DoesNotExist:
#             raise ValueError("Profile does not exist for user")
#         context = {
#             'profile': r_profile
#         }
        
#         if request.method == 'POST':
#             name = request.POST.get('name')
#             image_profile = request.FILES.get('image_profile')
#             shortBio = request.POST.get('shortBio')
#             detail = request.POST.get('detail')
#             github = request.POST.get('github')
#             youtube = request.POST.get('youtube')
#             twitter = request.POST.get('twitter')
#             facebook = request.POST.get('facebook')
#             instagram = request.POST.get('instagram')
#             linkedin = request.POST.get('linkedin')
           
            

#             try:
#                 r_profile = ProfileProject.objects.get(user=request.user)
#             except ProfileProject.DoesNotExist:
#                 raise ValueError("Profile does not exist for user")
#             r_profile.name=name    
#             r_profile.image_profile=image_profile
#             r_profile.shortBio=shortBio
#             r_profile.github=github
#             r_profile.youtube=youtube
#             r_profile.twitter=twitter
#             r_profile.facebook=facebook
#             r_profile.instagram=instagram
#             r_profile.linkedin=linkedin

#             r_profile.save()
#             if(r_profile.status=="Student"):
#                 date_of_birth = request.POST.get('date_of_birth')
#                 department = request.POST.get('department')
#                 student = Student.objects.filter(profile=r_profile)

#                 if student.exists():
#                     student=Student.objects.get(profile=r_profile)
#                 else:
#                     student=Student()  
                
#                 student.profile = r_profile
#                 student.department = department
#                 if(date_of_birth is not None ):
#                     student.date_of_birth = date_of_birth
#                 student.save()
#                 return redirect('userauths:profile_detail',profile_id=r_profile.id)   



#             elif(r_profile.status=="Teacher"):
#                 date_of_birth = request.POST.get('date_of_birth')
#                 department = request.POST.get('department')
#                 qualification = request.POST.get('qualification')
#                 bio = request.POST.get('bio')
#                 research_interests = request.POST.get('research_interests')
#                 teacher = Teacher.objects.filter(profile=r_profile)

#                 if teacher.exists():
#                     teacher=Teacher.objects.get(profile=r_profile)
#                 else:
#                     teacher=Teacher()  
                 
#                 teacher.profile = r_profile
#                 teacher.department = department
#                 teacher.qualification = qualification
#                 teacher.bio = bio
#                 teacher.research_interests = research_interests

#                 if(date_of_birth is not None ):
#                     teacher.date_of_birth = date_of_birth
#                 teacher.save()
#                 return redirect('userauths:profile_detail',profile_id=r_profile.id)  
            

#             elif(r_profile.status=="Organization"):
#                 location=request.POST.get('location')
#                 website = request.POST.get('website')
#                 founded_year = request.POST.get('founded_year')
#                 employees = request.POST.get('employees')

#                 organization = Organization.objects.filter(profile=r_profile)
#                 if organization.exists():
#                     organization=Organization.objects.get(profile=r_profile)
#                 else:
#                     organization=Organization()  
#                 organization.profile = r_profile
#                 organization.location = location
#                 organization.website = website
#                 organization.employees = employees

#                 if(founded_year is not "" ):
#                     organization.founded_year = founded_year
#                 organization.save()
#                 return redirect('userauths:profile_detail',profile_id=r_profile.id)   
#             else:
#                 return HttpResponse("Something went wrong")
#         return render(request, 'user/update_profile.html', context)
#     else:
#         return redirect('index')
    

# def profile_detail(request, profile_id):
    
#     profile = get_object_or_404(ProfileProject, id=profile_id)
    
#     if profile.status == 'Organization':
#         organization = get_object_or_404(Organization, profile=profile)
#         context = {'organization': organization,'profile': profile}
    
#     elif profile.status == 'Teacher':
#         teacher = get_object_or_404(Teacher, profile=profile)
#         context = {'teacher': teacher,'profile': profile}
    
#     else:
#         student = get_object_or_404(Student, profile=profile)
#         context = {'student': student,'profile': profile}
#     return render(request, 'user/user_details.html', context)    


