from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    negara = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'negara']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None
        del self.fields['password2']