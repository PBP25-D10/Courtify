from django.shortcuts import render, redirect, get_object_or_404
from authentication.decorators import penyedia_required
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import Lapangan
from .forms import LapanganForm
from booking.models import Booking
import json


def _json_error(message, status=400):
    return JsonResponse({'status': 'error', 'message': message}, status=status)


def _validate_penyedia(request, forbidden_message=None):
    if not request.user.is_authenticated:
        return _json_error('Not authenticated', status=401)
    try:
        if request.user.userprofile.role != 'penyedia':
            message = forbidden_message or 'Only penyedia can access this'
            return _json_error(message, status=403)
    except AttributeError:
        return _json_error('User profile not found', status=403)
    return None


def _serialize_lapangan(lapangan):
    if lapangan.url_thumbnail:
        thumb = lapangan.url_thumbnail
    elif lapangan.foto:
        thumb = lapangan.foto.url
    else:
        thumb = DEFAULT_LAPANGAN_IMAGE
    return {
        'id': str(lapangan.id_lapangan),
        'id_lapangan': str(lapangan.id_lapangan),
        'nama': lapangan.nama,
        'deskripsi': lapangan.deskripsi,
        'kategori': lapangan.kategori,
        'lokasi': lapangan.lokasi,
        'harga_per_jam': lapangan.harga_per_jam,
        'foto': thumb,
        'jam_buka': lapangan.jam_buka.strftime("%H:%M:%S"),
        'jam_tutup': lapangan.jam_tutup.strftime("%H:%M:%S"),
    }


def _normalize_payload(payload):
    if not isinstance(payload, dict):
        return QueryDict('', mutable=True)
    payload = payload.copy()
    if isinstance(payload.get('foto'), str):
        payload.pop('foto', None)
    query_dict = QueryDict('', mutable=True)
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, list):
            query_dict.setlist(key, [str(item) for item in value])
        else:
            if key in ('jam_buka', 'jam_tutup'):
                value = _normalize_time(value)
            query_dict[key] = str(value)
    return query_dict


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
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{field}: {error}")
                return JsonResponse({
                    "status": "error", 
                    "message": "; ".join(error_messages)
                })
            except Exception as exc:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Terjadi kesalahan: {str(exc)}"
                }, status=500)
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
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{field}: {error}")
                return JsonResponse({
                    "status": "error", 
                    "message": "; ".join(error_messages)
                })
            except Exception as exc:
                return JsonResponse({
                    "status": "error", 
                    "message": f"Terjadi kesalahan: {str(exc)}"
                }, status=500)
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
            return JsonResponse({
                'status': 'error',
                'message': 'Anda tidak memiliki izin untuk menghapus lapangan ini'
            }, status=403)
        except Exception as exc:
            return JsonResponse({
                'status': 'error',
                'message': f'Error: {str(exc)}'
            }, status=500)


@csrf_exempt
def flutter_api_list_lapangan(request):
    if request.method != 'GET':
        return _json_error('Method not allowed', status=405)

    auth_error = _validate_penyedia(request)
    if auth_error:
        return auth_error

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

    data = [_serialize_lapangan(lapangan) for lapangan in lapangan_list]
    return JsonResponse({'status': 'success', 'lapangan_list': data})


@csrf_exempt
def flutter_api_create_lapangan(request):
    if request.method != 'POST':
        return _json_error('Method not allowed', status=405)

    auth_error = _validate_penyedia(request, 'Only penyedia can create lapangan')
    if auth_error:
        return auth_error

    try:
        form_data = request.POST
        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body.decode('utf-8') or '{}')
            except json.JSONDecodeError:
                return _json_error('Invalid JSON', status=400)
            form_data = _normalize_payload(payload)

        form = LapanganForm(form_data, request.FILES)
        if form.is_valid():
            lapangan = form.save(commit=False)
            lapangan.owner = request.user
            lapangan.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Lapangan berhasil ditambahkan',
                'lapangan': _serialize_lapangan(lapangan)
            })

        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        return _json_error('; '.join(error_messages), status=400)
    except Exception as exc:
        return _json_error(f'Terjadi kesalahan: {str(exc)}', status=500)


@csrf_exempt
def flutter_api_update_lapangan(request, id_lapangan):
    if request.method != 'POST':
        return _json_error('Method not allowed', status=405)

    auth_error = _validate_penyedia(request, 'Only penyedia can update lapangan')
    if auth_error:
        return auth_error

    try:
        lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
        if lapangan.owner != request.user:
            return _json_error('You do not own this lapangan', status=403)

        form_data = request.POST
        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body.decode('utf-8') or '{}')
            except json.JSONDecodeError:
                return _json_error('Invalid JSON', status=400)
            form_data = _normalize_payload(payload)

        form = LapanganForm(form_data, request.FILES, instance=lapangan)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Lapangan berhasil diperbarui',
                'lapangan': _serialize_lapangan(lapangan)
            })

        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        return _json_error('; '.join(error_messages), status=400)
    except Exception as exc:
        return _json_error(f'Error: {str(exc)}', status=500)


@csrf_exempt
def flutter_api_delete_lapangan(request, id_lapangan):
    if request.method != 'POST':
        return _json_error('Method not allowed', status=405)

    auth_error = _validate_penyedia(request, 'Only penyedia can delete lapangan')
    if auth_error:
        return auth_error

    try:
        lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
        if lapangan.owner != request.user:
            return _json_error('You do not own this lapangan', status=403)

        lapangan.delete()
        return JsonResponse({'status': 'success', 'message': 'Lapangan berhasil dihapus'})
    except Exception as exc:
        return _json_error(f'Error: {str(exc)}', status=500)


@csrf_exempt
def flutter_api_public_list_lapangan(request):
    if request.method != 'GET':
        return _json_error('Method not allowed', status=405)

    kategori = request.GET.get('kategori', '')
    lokasi = request.GET.get('lokasi', '')
    harga_min = request.GET.get('harga_min', '')
    harga_max = request.GET.get('harga_max', '')

    lapangan_list = Lapangan.objects.all()

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

    data = [_serialize_lapangan(lapangan) for lapangan in lapangan_list]
    return JsonResponse({'status': 'success', 'lapangan_list': data})


@csrf_exempt
def flutter_api_detail_lapangan(request, id_lapangan):
    if request.method != 'GET':
        return _json_error('Method not allowed', status=405)

    lapangan = get_object_or_404(Lapangan, pk=id_lapangan)
    return JsonResponse({'status': 'success', 'lapangan': _serialize_lapangan(lapangan)})


@csrf_exempt
def flutter_api_get_penyedia_lapangan(request, penyedia_id):
    if request.method != 'GET':
        return _json_error('Method not allowed', status=405)

    user_model = get_user_model()
    penyedia = get_object_or_404(user_model, pk=penyedia_id)
    lapangan_list = Lapangan.objects.filter(owner=penyedia)
    data = [_serialize_lapangan(lapangan) for lapangan in lapangan_list]
    return JsonResponse(data, safe=False)


@csrf_exempt
def flutter_api_upload_foto_lapangan(request, id_lapangan):
    if request.method != "POST":
        return _json_error("Method not allowed", status=405)

    auth_error = _validate_penyedia(request, 'Only penyedia can upload photos')
    if auth_error:
        return auth_error

    lapangan = get_object_or_404(Lapangan, pk=id_lapangan)

    if lapangan.owner != request.user:
        return _json_error("You do not own this lapangan", status=403)

    if "foto" not in request.FILES:
        return _json_error("Field 'foto' wajib dikirim sebagai file", status=400)

    lapangan.foto = request.FILES["foto"]
    lapangan.save()

    return JsonResponse({
        "status": "success",
        "message": "Foto berhasil diupload",
        "foto": lapangan.foto.url if lapangan.foto else None
    })
DEFAULT_LAPANGAN_IMAGE = "https://images.pexels.com/photos/17724042/pexels-photo-17724042.jpeg"


def _normalize_time(val):
    if isinstance(val, str) and len(val) == 8 and val.count(':') == 2 and val.endswith(':00'):
        return val[:5]
    return val
