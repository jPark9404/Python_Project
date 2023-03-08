from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=20)
    content = forms.CharField(max_length=500, widget=forms.Textarea)
  
