from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Booking
from lapangan.models import Lapangan
from .forms import BookingForm


def _json_error(message, status=400):
    return JsonResponse({'success': False, 'message': message}, status=status)


def _serialize_lapangan(lap):
    return {
        'id_lapangan': str(lap.id_lapangan),
        'nama': lap.nama,
        'kategori': lap.kategori,
        'lokasi': lap.lokasi,
        'harga_per_jam': int(lap.harga_per_jam) if lap.harga_per_jam else 0,
        'jam_buka': str(lap.jam_buka),
        'jam_tutup': str(lap.jam_tutup),
        'foto_url': lap.foto.url if lap.foto else None,
    }


def _serialize_booking(booking):
    return {
        'id': int(booking.id),
        'lapangan': _serialize_lapangan(booking.lapangan) if booking.lapangan else None,
        'tanggal': str(booking.tanggal),
        'jam_mulai': str(booking.jam_mulai),
        'jam_selesai': str(booking.jam_selesai),
        'total_harga': float(booking.total_harga) if booking.total_harga else 0.0,
        'status': str(booking.status),
        'created_at': booking.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }


def _compute_total_harga(lapangan, jam_mulai_str, jam_selesai_str):
    try:
        start = datetime.strptime(jam_mulai_str, "%H:%M").time()
        end = datetime.strptime(jam_selesai_str, "%H:%M").time()
    except ValueError:
        return None
    duration = datetime.combine(datetime.today(), end) - datetime.combine(datetime.today(), start)
    hours = max(int(duration.total_seconds() // 3600), 0)
    return lapangan.harga_per_jam * hours


@login_required
def booking_dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    lapangan_list = Lapangan.objects.all().order_by('nama')[:5]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        data = {
            'status': 'success',
            'bookings': [_serialize_booking(b) for b in bookings],
            'lapangan_list': [_serialize_lapangan(l) for l in lapangan_list]
        }
        return JsonResponse(data)

    return render(request, 'booking/dashboard.html', {
        'bookings': bookings,
        'lapangan_list': lapangan_list
    })


@login_required
def booking_list_view(request):
    lapangan_list = Lapangan.objects.all().order_by('nama')

    search = request.GET.get('search')
    kategori = request.GET.get('kategori')
    harga_min = request.GET.get('harga_min')
    harga_max = request.GET.get('harga_max')

    if search:
        lapangan_list = lapangan_list.filter(Q(nama__icontains=search) | Q(lokasi__icontains=search))
    if kategori:
        lapangan_list = lapangan_list.filter(kategori__icontains=kategori)
    if harga_min:
        lapangan_list = lapangan_list.filter(harga_per_jam__gte=harga_min)
    if harga_max:
        lapangan_list = lapangan_list.filter(harga_per_jam__lte=harga_max)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = [{
            'id_lapangan': lap.id_lapangan,
            'nama': lap.nama,
            'kategori': lap.kategori,
            'lokasi': lap.lokasi,
            'harga_per_jam': lap.harga_per_jam,
            'jam_buka': str(lap.jam_buka),
            'jam_tutup': str(lap.jam_tutup),
            'foto_url': lap.foto.url if lap.foto else None,
            'iklan_id': lap.iklans.first().id if lap.iklans.exists() else None,
        } for lap in lapangan_list]
        return JsonResponse({'lapangan_list': data})

    return render(request, 'booking/booking_list.html', {'lapangan_list': lapangan_list})


@login_required
def booking_create_view(request, id_lapangan=None):
    lapangan_terpilih = None
    if id_lapangan:
        lapangan_terpilih = get_object_or_404(Lapangan, id_lapangan=id_lapangan)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            if lapangan_terpilih:
                booking.lapangan = lapangan_terpilih
            booking.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})

            messages.success(request, 'Booking berhasil dibuat!')
            return redirect('booking:booking_dashboard')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        initial = {}
        if lapangan_terpilih:
            initial['lapangan'] = lapangan_terpilih
        form = BookingForm(initial=initial)

    jam_range = list(range(24))
    return render(request, 'booking/booking_form.html', {
        'form': form,
        'lapangan_terpilih': lapangan_terpilih,
        'jam_range': jam_range
    })


@login_required
def update_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Booking berhasil diperbarui!',
                    'booking': {
                        'id': booking.id,
                        'status': booking.status,
                    }
                })

            messages.success(request, 'Booking berhasil diperbarui!')
            return redirect('booking:booking_dashboard')

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/booking_form.html', {'form': form})


@login_required
def cancel_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    booking.status = 'cancelled'
    booking.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Booking telah dibatalkan.',
            'booking_id': booking.id
        })

    messages.warning(request, 'Booking telah dibatalkan.')
    return redirect('booking:booking_dashboard')


@login_required
def booking_user_list_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        data = {
            'status': 'success',
            'bookings': [_serialize_booking(b) for b in bookings]
        }
        return JsonResponse(data)

    return render(request, 'booking/booking_user_list.html', {'bookings': bookings})


@login_required
def confirm_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.user != booking.lapangan.owner:
        return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)

    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Booking telah dikonfirmasi.',
                'booking_id': booking.id
            })

        messages.success(request, 'Booking telah dikonfirmasi.')
        return redirect('lapangan:manajemen_dashboard')
    return JsonResponse({'success': False, 'message': 'Booking sudah diproses.'}, status=400)


@login_required
def get_booked_hours(request, lapangan_id, tanggal):
    bookings = Booking.objects.filter(
        lapangan_id=lapangan_id,
        tanggal=tanggal,
        status__in=['pending', 'confirmed']
    )

    jam_terpakai = []
    for booking in bookings:
        jam_terpakai.extend(range(booking.jam_mulai.hour, booking.jam_selesai.hour))

    jam_terpakai = sorted(set(jam_terpakai))

    return JsonResponse({'jam_terpakai': jam_terpakai})


@login_required
def api_booking_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    lapangan_list = Lapangan.objects.all().order_by('nama')[:5]

    return JsonResponse({
        'status': 'success',
        'bookings': [_serialize_booking(b) for b in bookings],
        'lapangan_list': [_serialize_lapangan(l) for l in lapangan_list],
    })


@login_required
def api_booking_user_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    return JsonResponse({
        'status': 'success',
        'bookings': [_serialize_booking(b) for b in bookings],
    })


@login_required
def api_create_booking(request, id_lapangan):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    lapangan = get_object_or_404(Lapangan, id_lapangan=id_lapangan)

    try:
        tanggal = request.POST.get('tanggal')
        jam_mulai = request.POST.get('jam_mulai')
        jam_selesai = request.POST.get('jam_selesai')
        total_harga = _compute_total_harga(lapangan, jam_mulai, jam_selesai)

        booking = Booking.objects.create(
            user=request.user,
            lapangan=lapangan,
            tanggal=tanggal,
            jam_mulai=jam_mulai,
            jam_selesai=jam_selesai,
            total_harga=total_harga,
            status='pending'
        )

        return JsonResponse({
            'success': True,
            'booking': _serialize_booking(booking)
        })

    except Exception as exc:
        return JsonResponse({'success': False, 'message': str(exc)}, status=400)


@login_required
def api_cancel_booking(request, booking_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'cancelled'
    booking.save()

    return JsonResponse({
        'success': True,
        'message': 'Booking dibatalkan',
        'booking_id': booking.id
    })


@login_required
def flutter_api_booking_list(request):
    if request.method != 'GET':
        return _json_error('Method not allowed', status=405)
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return JsonResponse({'success': True, 'bookings': [_serialize_booking(b) for b in bookings]})


@login_required
def flutter_api_create_booking(request, id_lapangan):
    if request.method != 'POST':
        return _json_error('Method not allowed', status=405)

    lapangan = get_object_or_404(Lapangan, id_lapangan=id_lapangan)

    try:
        if request.content_type and 'application/json' in request.content_type:
            payload = json.loads(request.body.decode('utf-8') or '{}')
            tanggal = payload.get('tanggal')
            jam_mulai = payload.get('jam_mulai')
            jam_selesai = payload.get('jam_selesai')
        else:
            tanggal = request.POST.get('tanggal')
            jam_mulai = request.POST.get('jam_mulai')
            jam_selesai = request.POST.get('jam_selesai')

        total_harga = _compute_total_harga(lapangan, jam_mulai, jam_selesai)
        if total_harga is None:
            return _json_error('Format waktu tidak valid', status=400)

        booking = Booking.objects.create(
            user=request.user,
            lapangan=lapangan,
            tanggal=tanggal,
            jam_mulai=jam_mulai,
            jam_selesai=jam_selesai,
            total_harga=total_harga,
            status='pending'
        )

        return JsonResponse({'success': True, 'booking': _serialize_booking(booking)}, status=201)
    except Exception as exc:
        return _json_error(str(exc), status=400)


@login_required
def flutter_api_cancel_booking(request, booking_id):
    if request.method != 'POST':
        return _json_error('Method not allowed', status=405)

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.status = 'cancelled'
    booking.save()
    return JsonResponse({'success': True, 'message': 'Booking dibatalkan', 'booking_id': booking.id})


@login_required
def flutter_api_confirm_booking(request, booking_id):
    if request.method != 'POST':
        return _json_error('Method not allowed', status=405)

    booking = get_object_or_404(Booking, id=booking_id)
    if request.user != booking.lapangan.owner:
        return _json_error('Unauthorized', status=403)

    if booking.status != 'pending':
        return _json_error('Booking sudah diproses.', status=400)

    booking.status = 'confirmed'
    booking.save()
    return JsonResponse({'success': True, 'message': 'Booking dikonfirmasi', 'booking_id': booking.id})


@csrf_exempt
def flutter_api_get_booked_hours(request, lapangan_id, tanggal):
    if request.method != 'GET':
        return _json_error('Method not allowed', status=405)

    bookings = Booking.objects.filter(
        lapangan_id=lapangan_id,
        tanggal=tanggal,
        status__in=['pending', 'confirmed']
    )

    jam_terpakai = []
    for booking in bookings:
        jam_terpakai.extend(range(booking.jam_mulai.hour, booking.jam_selesai.hour))

    jam_terpakai = sorted(set(jam_terpakai))
    return JsonResponse({'success': True, 'jam_terpakai': jam_terpakai})
