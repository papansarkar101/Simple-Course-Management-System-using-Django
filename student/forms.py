from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Course

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'user_type', 'bio',)



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description']