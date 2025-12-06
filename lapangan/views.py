from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.decorators import penyedia_required
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Lapangan
from .forms import LapanganForm
from booking.models import Booking
import json

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

    pending_bookings = Booking.objects.filter(
        lapangan__owner=request.user,
        status='pending'
    ).select_related('lapangan', 'user').order_by('-created_at')

    return render(request, 'manajemen_lapangan/manajemen_dashboard.html', {
        'lapangan_list': lapangan_list,
        'kategori_choices': Lapangan._meta.get_field('kategori').choices,
        'pending_bookings': pending_bookings
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
                'foto': lapangan.foto.url if lapangan.foto else None,
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
                            "foto": lapangan.foto.url if lapangan.foto else None
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
                            "foto": lapangan.foto.url if lapangan.foto else None
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

# ============================================
# FLUTTER API ENDPOINTS
# ============================================

@csrf_exempt
def flutter_api_list_lapangan(request):
    """API endpoint for Flutter to get list of lapangan for logged-in penyedia"""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    # Check if user is penyedia
    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can access this'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)
    
    # Get lapangan for this penyedia
    lapangan_list = Lapangan.objects.filter(owner=request.user)
    
    data = []
    for lapangan in lapangan_list:
        data.append({
            'id': str(lapangan.id_lapangan),
            'nama': lapangan.nama,
            'deskripsi': lapangan.deskripsi,
            'kategori': lapangan.kategori,
            'lokasi': lapangan.lokasi,
            'harga_per_jam': lapangan.harga_per_jam,
            'foto': lapangan.foto.url if lapangan.foto else None,
            'jam_buka': lapangan.jam_buka,
            'jam_tutup': lapangan.jam_tutup,
        })
    
    return JsonResponse({'status': 'success', 'lapangan_list': data})


@csrf_exempt
def flutter_api_create_lapangan(request):
    """API endpoint for Flutter to create new lapangan"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    # Check if user is penyedia
    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can create lapangan'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)
    
    try:
        form = LapanganForm(request.POST, request.FILES)
        if form.is_valid():
            lapangan = form.save(commit=False)
            lapangan.owner = request.user
            lapangan.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Lapangan berhasil ditambahkan',
                'lapangan': {
                    'id': str(lapangan.id_lapangan),
                    'nama': lapangan.nama,
                    'kategori': lapangan.kategori,
                    'lokasi': lapangan.lokasi,
                    'foto': lapangan.foto.url if lapangan.foto else None
                }
            })
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            return JsonResponse({
                'status': 'error',
                'message': '; '.join(error_messages)
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Terjadi kesalahan: {str(e)}'
        }, status=500)


@csrf_exempt
def flutter_api_update_lapangan(request, id_lapangan):
    """API endpoint for Flutter to update lapangan"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    # Check if user is penyedia
    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can update lapangan'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)
    
    try:
        lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
        
        # Check ownership
        if lapangan.owner != request.user:
            return JsonResponse({'status': 'error', 'message': 'You do not own this lapangan'}, status=403)
        
        form = LapanganForm(request.POST, request.FILES, instance=lapangan)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Lapangan berhasil diperbarui',
                'lapangan': {
                    'id': str(lapangan.id_lapangan),
                    'nama': lapangan.nama,
                    'kategori': lapangan.kategori,
                    'lokasi': lapangan.lokasi,
                    'foto': lapangan.foto.url if lapangan.foto else None
                }
            })
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            return JsonResponse({
                'status': 'error',
                'message': '; '.join(error_messages)
            }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error: {str(e)}'
        }, status=500)


@csrf_exempt
def flutter_api_delete_lapangan(request, id_lapangan):
    """API endpoint for Flutter to delete lapangan"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    # Check if user is penyedia
    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can delete lapangan'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)
    
    try:
        lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
        
        # Check ownership
        if lapangan.owner != request.user:
            return JsonResponse({'status': 'error', 'message': 'You do not own this lapangan'}, status=403)
        
        lapangan.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Lapangan berhasil dihapus'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error: {str(e)}'
        }, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

@csrf_exempt
def flutter_api_get_penyedia_lapangan(request, penyedia_id):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # 1. Ambil User berdasarkan ID yang dikirim Flutter
    User = get_user_model()
    # Menggunakan 'pk' agar fleksibel (bisa id integer atau uuid user)
    penyedia = get_object_or_404(User, pk=penyedia_id) 

    # 2. Filter lapangan milik user tersebut
    lapangan_list = Lapangan.objects.filter(owner=penyedia)
    
    # 3. Format data agar SAMA PERSIS dengan model Lapangan.fromJson di Flutter
    data = []
    for lapangan in lapangan_list:
        data.append({
            'id_lapangan': str(lapangan.id_lapangan),
            'nama': lapangan.nama,
            'deskripsi': lapangan.deskripsi,
            'kategori': lapangan.kategori,
            'lokasi': lapangan.lokasi,
            'harga_per_jam': lapangan.harga_per_jam,
            # Flutter code Anda menambahkan base url sendiri, jadi kirim path-nya saja
            # contoh: "/media/img/foto.jpg"
            'foto': lapangan.foto.url if lapangan.foto else None, 
            'jam_buka': lapangan.jam_buka.strftime("%H:%M:%S"), # Format waktu string
            'jam_tutup': lapangan.jam_tutup.strftime("%H:%M:%S"),
        })
    
    # PENTING: safe=False agar bisa me-return List JSON (Array) langsung
    # Ini cocok dengan kode Flutter: final List data = jsonDecode(response.body);
    return JsonResponse(data, safe=False)