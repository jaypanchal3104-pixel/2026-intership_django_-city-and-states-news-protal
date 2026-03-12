from django import forms
from core.models import News, Category, City


class NewsForm(forms.ModelForm):

    class Meta:
        model  = News
        fields = [
            'title',
            'description',
            'image',
            'category',
            'city',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class':       'form-control',
                'placeholder': 'Enter news title...',
            }),
            'description': forms.Textarea(attrs={
                'class':       'form-control',
                'rows':        10,
                'placeholder': 'Write full article here...',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'city': forms.Select(attrs={
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Journalist → draft/pending only
        # Admin      → badha status
        if user and user.role == 'journalist':
            self.fields['status'].choices = [
                ('draft',   'Save as Draft'),
                ('pending', 'Submit for Review'),
            ]

        self.fields['city'].required  = False
        self.fields['image'].required = False