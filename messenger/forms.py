from django import forms
from models import Massage, App, Wish, memeDef, Profile, bug_report, blog_post
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class message(forms.ModelForm):
    class Meta():
        model = Massage
        fields = ('text',)

class newApp(forms.ModelForm):
    class Meta():
        model = App
        fields = ('name', 'description', 'link')

class makeAWish(forms.ModelForm):
    class Meta():
        model = Wish
        fields = ('text',)

class memeDefForm(forms.ModelForm):
    class Meta():
        model = memeDef
        fields = ('name', 'definition', 'document')

class profileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('paypalEmail',)

class bugReportForm(forms.ModelForm):
    class Meta():
        model = bug_report
        fields = ('text',)

class blogPostForm(forms.ModelForm):
    class Meta():
        model = blog_post
        fields = ('title', 'text')