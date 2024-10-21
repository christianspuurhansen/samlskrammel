from django import forms

class CreateUserForm(forms.Form):
    your_name = forms.CharField(label="Brugernavn", max_length=100)
    your_email = forms.EmailField()
    your_pass = forms.CharField(label="Kodeord", max_length=100, widget=forms.PasswordInput())
    
class LoginForm(forms.Form):
    your_name = forms.CharField(label="Brugernavn", max_length=100)
    your_pass = forms.CharField(label="Kodeord", max_length=100, widget=forms.PasswordInput())

class CreatePostForm(forms.Form):
  field_what = forms.CharField(label="Hvad er samlet", max_length=100)
  field_weight = forms.DecimalField(label="Hvor mange kilo er samlet")
  field_image = forms.ImageField(label='Billede af indsamling', required=False)
  field_lat = forms.DecimalField(label='Opsamlings breddegrad')
  field_lon = forms.DecimalField(label='Opsamlings højdegrad')

class TilfoejVen(forms.Form):
    friend_name = forms.CharField(label="Vens Brugernavn", max_length=100)

