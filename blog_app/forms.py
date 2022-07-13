from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_slug, validate_image_file_extension
from django.forms import ModelForm, CharField, ImageField
from django import forms
from .models import Post, Comment


class PostForm(ModelForm):
    images = ImageField(validators=[validate_image_file_extension], required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'images', ]
    #
    # def create(self, user):
    #


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=150)
    password = forms.CharField(label='password', max_length=150)

    def save(self):
        d = self.cleaned_data
        user = authenticate(
            username=d['username'],
            password=d['password']
        )
        return user


class RegisterForm(forms.Form):
    email = forms.EmailField(label='email', )
    username = forms.CharField(label='username', max_length=150)
    password = forms.CharField(label='password', max_length=150)

    def create(self):
        d = self.cleaned_data
        user = User.objects.create_user(
            email=d['email'],
            username=d['username'],
            password=d['password'],
        )
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
