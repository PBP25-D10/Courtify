from django import forms
from .models import Iklan

class IklanForm(forms.ModelForm):
    class Meta:
        model = Iklan
        fields = ["lapangan", "date", "banner"]
