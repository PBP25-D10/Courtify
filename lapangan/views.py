# manajemen_lapangan/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.decorators import penyedia_required
from .models import Lapangan

@penyedia_required
def manajemen_dashboard_view(request):
    lapangan_list = Lapangan.objects.all()
    return render(request, 'manajemen_lapangan/manajemen_dashboard.html', {'lapangan_list': lapangan_list})


@penyedia_required
def lapangan_list_view(request):
    lapangan_list = Lapangan.objects.all()
    return render(request, 'manajemen_lapangan/lapangan_list.html', {'lapangan_list': lapangan_list})

@penyedia_required
def lapangan_create_view(request):
    kategori_choices = Lapangan._meta.get_field('kategori').choices

    if request.method == 'POST':
        nama = request.POST.get('nama')
        deskripsi = request.POST.get('deskripsi')
        kategori = request.POST.get('kategori')
        lokasi = request.POST.get('lokasi')
        harga_per_jam = request.POST.get('harga_per_jam') or 0
        foto = request.FILES.get('foto')
        jam_buka = request.POST.get('jam_buka')
        jam_tutup = request.POST.get('jam_tutup')

        # Validasi sederhana
        if not nama:
            messages.error(request, "Nama lapangan harus diisi.")
        else:
            Lapangan.objects.create(
                nama=nama,
                deskripsi=deskripsi,
                kategori=kategori,
                lokasi=lokasi,
                harga_per_jam=harga_per_jam,
                foto=foto,
                jam_buka=jam_buka,
                jam_tutup=jam_tutup,
            )
            messages.success(request, "Lapangan berhasil ditambahkan.")
            return redirect('manajemen_lapangan:lapangan_list_owner')

    context = {'kategori_choices': kategori_choices, 'lapangan': None}
    return render(request, 'manajemen_lapangan/lapangan_create.html', context)

@penyedia_required
def lapangan_edit_view(request, id_lapangan):
    lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
    kategori_choices = Lapangan._meta.get_field('kategori').choices

    if request.method == 'POST':
        lapangan.nama = request.POST.get('nama')
        lapangan.deskripsi = request.POST.get('deskripsi')
        lapangan.kategori = request.POST.get('kategori')
        lapangan.lokasi = request.POST.get('lokasi')
        lapangan.harga_per_jam = request.POST.get('harga_per_jam') or lapangan.harga_per_jam
        if request.FILES.get('foto'):
            lapangan.foto = request.FILES.get('foto')
        lapangan.jam_buka = request.POST.get('jam_buka')
        lapangan.jam_tutup = request.POST.get('jam_tutup')
        lapangan.save()
        messages.success(request, "Lapangan berhasil diperbarui.")
        return redirect('manajemen_lapangan:lapangan_list_owner')

    context = {'kategori_choices': kategori_choices, 'lapangan': lapangan}
    return render(request, 'manajemen_lapangan/lapangan_create.html', context)

@penyedia_required
def lapangan_delete_view(request, id_lapangan):
    lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
    lapangan.delete()
    messages.success(request, "Lapangan berhasil dihapus.")
    return redirect('manajemen_lapangan:lapangan_list_owner')
