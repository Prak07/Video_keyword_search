from django import forms


class LoginForm(forms.Form):
    username=forms.CharField(label="Username",max_length=20)
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    
class SignupForm(forms.Form):
    username=forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
class ChangePassForm(forms.Form):
    old_password =forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
class EmailForm(forms.Form):
    email = forms.EmailField()
    
class NewPassForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


