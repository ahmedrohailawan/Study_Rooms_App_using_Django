from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields, ModelForm
from Home.models import Room, Topic,User


class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['avatar','username','email','bio']


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ('__all__')
        exclude = ['host','participants']

    def __init__(self,*args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['topics'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
