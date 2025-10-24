from django import forms
from .models import Lapangan

class LapanganForm(forms.ModelForm):
    class Meta:
        model = Lapangan
        fields = ['nama', 'deskripsi', 'kategori', 'lokasi', 'harga_per_jam', 'foto', 'jam_buka', 'jam_tutup']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Nama Lapangan'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Deskripsi lapangan...',
                'rows': 4
            }),
            'kategori': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'lokasi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Alamat lengkap lapangan'
            }),
            'harga_per_jam': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Harga per jam',
                'min': '0'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'accept': 'image/*'
            }),
            'jam_buka': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'time',
                'step': '3600',
                'min': '00:00',
                'max': '23:00'
            }),
            'jam_tutup': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'type': 'time',
                'step': '3600',
                'min': '00:00',
                'max': '23:00'
            }),
        }
        labels = {
            'nama': 'Nama Lapangan',
            'deskripsi': 'Deskripsi',
            'kategori': 'Kategori Olahraga',
            'lokasi': 'Lokasi',
            'harga_per_jam': 'Harga per Jam (Rp)',
            'foto': 'Foto Lapangan',
            'jam_buka': 'Jam Buka',
            'jam_tutup': 'Jam Tutup',
        }

    def clean(self):
        cleaned_data = super().clean()
        jam_buka = cleaned_data.get('jam_buka')
        jam_tutup = cleaned_data.get('jam_tutup')

        if jam_buka and jam_tutup:
            if jam_tutup <= jam_buka:
                raise forms.ValidationError('Jam tutup harus lebih besar dari jam buka.')

        return cleaned_data
