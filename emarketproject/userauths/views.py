from django.shortcuts import redirect, render
from userauths.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.conf import settings

User = settings.AUTH_USER_MODEL

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
        except:
            messages.warning(request, f"User with  the email address {email} does not exist.")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You are logged in as {user.username}")
            return redirect("core:index")
        
        else:
            messages.warning(request, "User does not exist. Create new account!")
    context = {

    }
        
    return render(request, "userauths/signIn.html", context)

