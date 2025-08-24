from django import forms
from django.contrib.auth.models import User
from .models import (
    TimetableEntry, Advertisement, News, Memo, Reel, Hostel,
    Religion, Politics, Music
)
from django import forms
from .models import Confession

class ConfessionForm(forms.ModelForm):
    class Meta:
        model = Confession
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your confession here...'})
        }

# ====================== Auth Forms ======================

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    remember_me = forms.BooleanField(required=False, initial=False, label="Remember Me")
    passwordless = forms.BooleanField(required=False, initial=False, label="Passwordless Login")

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def get_user(self):
        from django.contrib.auth import authenticate
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        return authenticate(self.request, username=username, password=password)


# ====================== PDF Upload Form ======================

class PDFUploadForm(forms.Form):
    timetable_pdf = forms.FileField(label="Upload Timetable PDF")


# ====================== Admin Forms ======================

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff']


# ====================== Content Forms ======================

def optional_file_field(field):
    """
    Sets required=False for file/image/audio fields for editing purposes
    """
    if isinstance(field.widget, (forms.ClearableFileInput,)):
        field.required = False
    return field

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            optional_file_field(field)

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = '__all__'

class ReelForm(forms.ModelForm):
    class Meta:
        model = Reel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            optional_file_field(field)

class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = '__all__'


# ====================== Admin Panel Category Forms ======================

class ReligionForm(forms.ModelForm):
    class Meta:
        model = Religion
        fields = '__all__'

class PoliticsForm(forms.ModelForm):
    class Meta:
        model = Politics
        fields = '__all__'

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            optional_file_field(field)
