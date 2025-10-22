from django import forms
from .models import Booking
from lapangan.models import Lapangan

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'lapangan',
            'tanggal',
            'jam_mulai',
            'jam_selesai',
            'total_harga',
        ]
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
            'jam_mulai': forms.TimeInput(attrs={'type': 'time'}),
            'jam_selesai': forms.TimeInput(attrs={'type': 'time'}),
        }

    # User tidak dimasukkan ke form karena otomatis diisi dari user yang login
    # Lapangan diambil dari model Lapangan (dropdown)
    lapangan = forms.ModelChoiceField(
        queryset=Lapangan.objects.all(),
        label="Pilih Lapangan"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ini opsional, tapi memastikan dropdown menampilkan nama
        self.fields['lapangan'].label_from_instance = lambda obj: obj.nama
