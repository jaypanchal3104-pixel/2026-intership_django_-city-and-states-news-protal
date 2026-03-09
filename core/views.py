from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import UserSignupForm, UserLoginForm


# ─────────────────────────────────────────────
#  SIGNUP VIEW
# ─────────────────────────────────────────────
def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST or None)

        if form.is_valid():
            user = form.save()

            # ── Send HTML Welcome Email ──────────────────────────
            try:
                email = form.cleaned_data['email']

                # Render the HTML email template
                html_content = render_to_string(
                    'core/welcome_email.html',
                    {
                        'user': user,
                        'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000'),
                        'unsubscribe_url': '#',
                    }
                )
                plain_text = strip_tags(html_content)  # plain-text fallback

                msg = EmailMultiAlternatives(
                    subject="Welcome to City & State News Portal",
                    body=plain_text,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)   # fail_silently=True so signup still works even if email fails

            except Exception:
                pass  # Do not block signup if email fails
            # ────────────────────────────────────────────────────

            return redirect('login')

        else:
            return render(request, 'core/signup.html', {'form': form})

    else:
        form = UserSignupForm()
        return render(request, 'core/signup.html', {'form': form})


# ─────────────────────────────────────────────
#  LOGIN VIEW
# ─────────────────────────────────────────────
def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # AbstractBaseUser with USERNAME_FIELD = 'email'
            # → pass email as the 'username' kwarg to authenticate()
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                # ── Role-based redirect ──────────────────────────
                role = user.role

                if role == "admin":
                    return redirect("admin_dashboard")

                elif role == "journalist":
                    return redirect("journalist_dashboard")

                elif role == "advertiser":
                    return redirect("advertiser_dashboard")

                else:
                    # 'user' role (reader) → home page
                    return redirect("home")
                # ────────────────────────────────────────────────

            else:
                form.add_error(None, "Invalid Email or Password. Please try again.")

        return render(request, 'core/login.html', {'form': form})

    else:
        form = UserLoginForm()
        return render(request, 'core/login.html', {'form': form})



def userLogoutView(request):
    logout(request)
    return redirect('login')