from django import forms

from django import forms

class CustomerServiceSearchForm(forms.Form):
    city = forms.CharField(max_length=30, required=False)
    category = forms.CharField(max_length=30, required=False)

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=150)   

class OTPVerificationForm(forms.Form):
    username = forms.CharField(max_length=150)
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'autocomplete': 'off'}))     

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email')

class OTPForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)    
