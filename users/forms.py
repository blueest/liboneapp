# forms.py
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'background_image', 'bio', 'phone_number', 'address', 'job', 'hobbies']
