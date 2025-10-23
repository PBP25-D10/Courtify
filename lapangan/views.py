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
    kategori = request.GET.get('kategori', '')
    lokasi = request.GET.get('lokasi', '')
    harga_min = request.GET.get('harga_min', '')
    harga_max = request.GET.get('harga_max', '')
    
    lapangan_list = Lapangan.objects.filter(owner=request.user)
    
    if kategori:
        lapangan_list = lapangan_list.filter(kategori=kategori)
    if lokasi:
        lapangan_list = lapangan_list.filter(lokasi__icontains=lokasi)
    if harga_min:
        try:
            lapangan_list = lapangan_list.filter(harga_per_jam__gte=int(harga_min))
        except ValueError:
            pass
    if harga_max:
        try:
            lapangan_list = lapangan_list.filter(harga_per_jam__lte=int(harga_max))
        except ValueError:
            pass
    
    return render(request, 'manajemen_lapangan/manajemen_dashboard.html', {
        'lapangan_list': lapangan_list,
        'kategori_choices': Lapangan._meta.get_field('kategori').choices
    })


@penyedia_required
def lapangan_list_view(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        kategori = request.GET.get('kategori', '')
        lokasi = request.GET.get('lokasi', '')
        harga_min = request.GET.get('harga_min', '')
        harga_max = request.GET.get('harga_max', '')
        
        lapangan_list = Lapangan.objects.filter(owner=request.user)
        
        if kategori:
            lapangan_list = lapangan_list.filter(kategori=kategori)
        if lokasi:
            lapangan_list = lapangan_list.filter(lokasi__icontains=lokasi)
        if harga_min:
            try:
                lapangan_list = lapangan_list.filter(harga_per_jam__gte=int(harga_min))
            except ValueError:
                pass
        if harga_max:
            try:
                lapangan_list = lapangan_list.filter(harga_per_jam__lte=int(harga_max))
            except ValueError:
                pass
        
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
            try:
                form = LapanganForm(request.POST, request.FILES)
                if form.is_valid():
                    lapangan = form.save(commit=False)
                    lapangan.owner = request.user
                    lapangan.save()
                    return JsonResponse({
                        "status": "success", 
                        "message": "Lapangan berhasil ditambahkan", 
                        "lapangan": {
                            "id": str(lapangan.id_lapangan), 
                            "nama": lapangan.nama, 
                            "kategori": lapangan.kategori, 
                            "lokasi": lapangan.lokasi, 
                            "foto_url": lapangan.foto.url if lapangan.foto else None
                        }
                    })
                else:
                    error_messages = []
                    for field, errors in form.errors.items():
                        for error in errors:
                            error_messages.append(f"{field}: {error}")
                    return JsonResponse({
                        "status": "error", 
                        "message": "; ".join(error_messages)
                    })
            except Exception as e:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Terjadi kesalahan: {str(e)}"
                }, status=500)
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
            try:
                form = LapanganForm(request.POST, request.FILES, instance=lapangan)
                if form.is_valid():
                    form.save()
                    return JsonResponse({
                        "status": "success", 
                        "message": "Lapangan berhasil diperbarui", 
                        "lapangan": {
                            "id": str(lapangan.id_lapangan), 
                            "nama": lapangan.nama, 
                            "kategori": lapangan.kategori, 
                            "lokasi": lapangan.lokasi, 
                            "foto_url": lapangan.foto.url if lapangan.foto else None
                        }
                    })
                else:
                    error_messages = []
                    for field, errors in form.errors.items():
                        for error in errors:
                            error_messages.append(f"{field}: {error}")
                    return JsonResponse({
                        "status": "error", 
                        "message": "; ".join(error_messages)
                    })
            except Exception as e:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Terjadi kesalahan: {str(e)}"
                }, status=500)
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
