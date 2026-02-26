from django.shortcuts import render,redirect
from .forms import UserSignupForm,UserLoginForm

from django.contrib.auth import authenticate, login

# Create your views here.
def userSignupView(request):
    if request.method =="POST":
      form = UserSignupForm(request.POST or None)
      if form.is_valid():
        form.save()
        return redirect('login') #error
      else:
        return render(request,'core/signup.html',{'form':form})  
    else:
        form = UserSignupForm()
        return render(request,'core/signup.html',{'form':form})

def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                # 👇 Role Based Redirect
                if user.role == "admin":
                    return redirect("admin_dashboard")

                elif user.role == "editor":
                    return redirect("editor_dashboard")

                elif user.role == "reporter":
                    return redirect("reporter_dashboard")

                elif user.role == "user":
                    return redirect("user_dashboard")

            else:
                form.add_error(None, "Invalid Email or Password")

        return render(request, 'core/login.html', {'form': form})

    else:
        form = UserLoginForm()
        return render(request, 'core/login.html', {'form': form})