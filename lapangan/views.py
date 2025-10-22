from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from authentication.decorators import penyedia_required  # Import dari authentication
from .models import Lapangan
from .forms import LapanganForm

@login_required
@penyedia_required
def manajemen_dashboard_view(request):
    """Dashboard untuk manajemen lapangan"""
    lapangan_list = Lapangan.objects.filter(owner=request.user.userprofile).order_by('-id_lapangan')
    context = {
        'lapangan_list': lapangan_list
    }
    return render(request, 'lapangan/manajemen_dashboard.html', context)

@login_required
@penyedia_required
def lapangan_list_view(request):
    lapangan_list = Lapangan.objects.filter(owner=request.user).order_by('-id_lapangan')
    context = {
        'lapangan_list': lapangan_list
    }
    return render(request, 'lapangan/lapangan_list_owner.html', context)

@login_required
@penyedia_required
def lapangan_detail_view(request, id_lapangan):
    lapangan = get_object_or_404(Lapangan, id_lapangan=id_lapangan, owner=request.user.userprofile)
    context = {
        'lapangan': lapangan
    }
    return render(request, 'lapangan/lapangan_detail.html', context)

@login_required
@penyedia_required
def lapangan_create_view(request):
    if request.method == 'POST':
        form = LapanganForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                lapangan = form.save(commit=False)
                lapangan.owner = request.user
                lapangan.save()
                
                # Check bila AJAX
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Lapangan berhasil ditambahkan!',
                        'lapangan_id': str(lapangan.id_lapangan)
                    })
                
                messages.success(request, 'Lapangan berhasil ditambahkan!')
                return redirect('lapangan:lapangan_list_owner')
            
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Terjadi kesalahan: {str(e)}'
                    }, status=400)
                messages.error(request, f'Terjadi kesalahan: {str(e)}')
        else:
            # Form tidak valid
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {}
                for field, error_list in form.errors.items():
                    errors[field] = [str(error) for error in error_list]
                return JsonResponse({
                    'status': 'error',
                    'message': 'Data tidak valid',
                    'errors': errors
                }, status=400)
            
            messages.error(request, 'Terjadi kesalahan pada form. Silakan periksa kembali.')
    else:
        form = LapanganForm()
    
    context = {
        'form': form,
        'title': 'Tambah Lapangan'
    }
    return render(request, 'lapangan/lapangan_form.html', context)

@login_required
@penyedia_required
def lapangan_edit_view(request, id_lapangan):
    lapangan = get_object_or_404(Lapangan, id_lapangan=id_lapangan, owner=request.user.userprofile)
    
    if request.method == 'POST':
        form = LapanganForm(request.POST, request.FILES, instance=lapangan)
        
        if form.is_valid():
            try:
                form.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Lapangan berhasil diupdate!'
                    })
                
                messages.success(request, 'Lapangan berhasil diupdate!')
                return redirect('lapangan:lapangan_list_owner')
            
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Terjadi kesalahan: {str(e)}'
                    }, status=400)
                messages.error(request, f'Terjadi kesalahan: {str(e)}')
        else:
            # Form tidak valid
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {}
                for field, error_list in form.errors.items():
                    errors[field] = [str(error) for error in error_list]
                return JsonResponse({
                    'status': 'error',
                    'message': 'Data tidak valid',
                    'errors': errors
                }, status=400)
            
            messages.error(request, 'Terjadi kesalahan pada form. Silakan periksa kembali.')
    else:
        form = LapanganForm(instance=lapangan)
    
    context = {
        'form': form,
        'lapangan': lapangan,
        'title': 'Edit Lapangan'
    }
    return render(request, 'lapangan/lapangan_form.html', context)

@login_required
@penyedia_required
@require_POST
def lapangan_delete_view(request, id_lapangan):
    try:
        lapangan = get_object_or_404(Lapangan, id_lapangan=id_lapangan, owner=request.user.userprofile)
        lapangan_nama = lapangan.nama
        lapangan.delete()
        
        # Check bila AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({
                'status': 'success',
                'message': f'Lapangan "{lapangan_nama}" berhasil dihapus!'
            })
        
        messages.success(request, f'Lapangan "{lapangan_nama}" berhasil dihapus!')
        return redirect('lapangan:lapangan_list_owner')
    
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': f'Terjadi kesalahan: {str(e)}'
            }, status=400)
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('lapangan:lapangan_list_owner')

@login_required
@penyedia_required
def lapangan_get_json(request, id_lapangan):
    #Endpoint JSON untuk AJAX GET - load data lapangan untuk edit form
    try:
        lapangan = get_object_or_404(Lapangan, id_lapangan=id_lapangan, owner=request.user.userprofile)
        data = {
            'id_lapangan': str(lapangan.id_lapangan),
            'nama': lapangan.nama,
            'deskripsi': lapangan.deskripsi,
            'kategori': lapangan.kategori,
            'kategori_display': lapangan.get_kategori_display(),
            'lokasi': lapangan.lokasi,
            'harga_per_jam': str(lapangan.harga_per_jam),
            'jam_buka': lapangan.jam_buka.strftime('%H:%M'),
            'jam_tutup': lapangan.jam_tutup.strftime('%H:%M'),
            'foto': lapangan.foto.url if lapangan.foto else None,
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=404)