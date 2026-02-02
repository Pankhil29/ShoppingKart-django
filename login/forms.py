from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' '
        })
    )
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': ' '
            })
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class':'form-control',
                'placeholder' : ' ',
            })



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'})
    )
    address = forms.CharField(
        required=False,
        max_length=1000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Yahan check karein ki kya user ke paas profile hai
        if self.instance and hasattr(self.instance, 'profile'):
            self.fields['phone'].initial = self.instance.profile.phone
            self.fields['address'].initial = self.instance.profile.address

    def save(self, commit=True):
        # 1. User ka asli data save karein (Username, Email, etc.)
        user = super().save(commit=False)
        if commit:
            user.save()
            # 2. Profile ka data save karein
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone')
            profile.address = self.cleaned_data.get('address')
            profile.save()
        return user
    