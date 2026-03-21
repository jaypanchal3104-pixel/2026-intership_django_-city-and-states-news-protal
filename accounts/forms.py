from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


# ─────────────────────────────────────────────
#  PROFILE EDIT FORM
# ─────────────────────────────────────────────
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['firstname', 'lastname', 'email', 'profile_photo']
        widgets = {
            'firstname':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'lastname':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email':         forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


# ─────────────────────────────────────────────
#  PASSWORD CHANGE FORM
# ─────────────────────────────────────────────
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Current Password'}
        )
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password'}
        )
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}
        )