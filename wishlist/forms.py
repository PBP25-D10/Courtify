# wishlist/forms.py
# Form untuk wishlist jika diperlukan, misalnya untuk menambah item
from django import forms
from .models import Wishlist

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['iklan']  # Hanya iklan yang dipilih
        widgets = {
            'iklan': forms.HiddenInput(),  # Hidden karena dipilih dari halaman lain
        }
