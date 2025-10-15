from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'nama_pemesan',
            'nama_lapangan',
            'tanggal',
            'jam_mulai',
            'jam_selesai',
            'total_harga',
        ]
    