from django.shortcuts import redirect, render
from userauths.forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import login, authenticate

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
