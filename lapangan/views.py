# manajemen_lapangan/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.decorators import penyedia_required
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from .models import Lapangan
from .forms import LapanganForm

@penyedia_required
def manajemen_dashboard_view(request):
    lapangan_list = Lapangan.objects.filter(owner=request.user)
    return render(request, 'manajemen_lapangan/manajemen_dashboard.html', {'lapangan_list': lapangan_list})


@penyedia_required
def lapangan_list_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        lapangan_list = Lapangan.objects.filter(owner=request.user)
        data = []
        for lapangan in lapangan_list:
            data.append({
                'id': lapangan.id_lapangan,
                'nama': lapangan.nama,
                'deskripsi': lapangan.deskripsi,
                'kategori': lapangan.kategori,
                'lokasi': lapangan.lokasi,
                'harga_per_jam': lapangan.harga_per_jam,
                'foto_url': lapangan.foto.url if lapangan.foto else None,
                'jam_buka': lapangan.jam_buka,
                'jam_tutup': lapangan.jam_tutup,
            })
        return JsonResponse({'lapangan_list': data})
    return render(request, 'manajemen_lapangan/lapangan_list.html')

@penyedia_required
def lapangan_create_view(request):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = LapanganForm(request.POST, request.FILES)
            if form.is_valid():
                lapangan = form.save(commit=False)
                lapangan.owner = request.user
                lapangan.save()
                return JsonResponse({"status": "success", "message": "Lapangan berhasil ditambahkan", "lapangan": {"id": lapangan.id_lapangan, "nama": lapangan.nama, "kategori": lapangan.kategori, "lokasi": lapangan.lokasi, "foto_url": lapangan.foto.url if lapangan.foto else None}})
            else:
                return JsonResponse({"status": "error", "message": form.errors.as_json()})
        else:
            form = LapanganForm(request.POST, request.FILES)
            if form.is_valid():
                lapangan = form.save(commit=False)
                lapangan.owner = request.user
                lapangan.save()
                return redirect('manajemen_lapangan:lapangan_list_owner')
    else:
        form = LapanganForm()
    return render(request, 'manajemen_lapangan/lapangan_create.html', {"form": form})

@penyedia_required
def lapangan_edit_view(request, id_lapangan):
    lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = LapanganForm(request.POST, request.FILES, instance=lapangan)
            if form.is_valid():
                form.save()
                return JsonResponse({"status": "success", "message": "Lapangan berhasil diperbarui", "lapangan": {"id": lapangan.id_lapangan, "nama": lapangan.nama, "kategori": lapangan.kategori, "lokasi": lapangan.lokasi, "foto_url": lapangan.foto.url if lapangan.foto else None}})
            else:
                return JsonResponse({"status": "error", "message": form.errors.as_json()})
        else:
            form = LapanganForm(request.POST, request.FILES, instance=lapangan)
            if form.is_valid():
                form.save()
                return redirect('manajemen_lapangan:lapangan_list_owner')
    else:
        form = LapanganForm(instance=lapangan)
    return render(request, 'manajemen_lapangan/lapangan_create.html', {"form": form})

@penyedia_required
def lapangan_delete_view(request, id_lapangan):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
            if request.user == lapangan.owner:
                lapangan.delete()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Lapangan berhasil dihapus'
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Anda tidak memiliki izin untuk menghapus lapangan ini'
                }, status=403)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error: {str(e)}'
            }, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
