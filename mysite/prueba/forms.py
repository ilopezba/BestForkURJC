from django import forms
from models import Articulo

class ArticuloForm(forms.ModelForm):

   class Meta:
      model = Articulo

class SettingsForm(forms.ModelForm):
    receive_newsletter = forms.BooleanField()

    class Meta:
        model = Settings
