from django import forms
from .models import Booking
from lapangan.models import Lapangan

class BookingForm(forms.ModelForm):
    lapangan = forms.ModelChoiceField(
        queryset=Lapangan.objects.all(),
        label="Pilih Lapangan"
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lapangan'].label_from_instance = lambda obj: obj.nama

        # Tambahkan atribut HTML 'data-harga' untuk setiap opsi
        choices = []
        for lap in self.fields['lapangan'].queryset:
            choices.append((lap.id_lapangan, f"{lap.nama} - Rp{lap.harga_per_jam:,}"))
        self.fields['lapangan'].choices = choices
