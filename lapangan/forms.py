from django import forms
from .models import Lapangan

class LapanganForm(forms.ModelForm):
    # Generate pilihan jam dari 00:00 sampai 23:00
    JAM_CHOICES = [(f'{i:02d}:00', f'{i:02d}:00') for i in range(24)]
    
    jam_buka = forms.ChoiceField(
        choices=JAM_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )
    
    jam_tutup = forms.ChoiceField(
        choices=JAM_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )
    
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
