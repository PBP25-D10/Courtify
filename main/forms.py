from django import forms
from lapangan.models import Lapangan
from .models import Iklan

class IklanForm(forms.ModelForm):
    class Meta:
        model = Iklan
        fields = ["lapangan","judul", "deskripsi", "banner", "url_thumbnail"]
        widgets = {
            'deskripsi': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['lapangan'].queryset = Lapangan.objects.filter(owner=user)
