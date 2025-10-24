# booking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Booking
from .models import Lapangan
from .forms import BookingForm

from django.db.models import Q


# 🏠 Dashboard Booking
@login_required
def booking_dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')[:5]
    lapangan_list = Lapangan.objects.all().order_by('nama')[:5]

    return render(request, 'booking/dashboard.html', {
        'bookings': bookings,
        'lapangan_list': lapangan_list
    })



# 📋 List Semua Booking (bisa untuk admin atau penyedia)
@login_required
def booking_list_view(request):
    lapangan_list = Lapangan.objects.all().order_by('nama')

    search = request.GET.get('search')
    kategori = request.GET.get('kategori')
    harga_min = request.GET.get('harga_min')
    harga_max = request.GET.get('harga_max')

    if search:
        lapangan_list = lapangan_list.filter(
            Q(nama__icontains=search) | Q(lokasi__icontains=search)
        )
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
            'iklan_id': lap.iklan_set.first().id if lap.iklan_set.exists() else None,
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
            messages.success(request, 'Booking berhasil dibuat!')
            return redirect('booking:booking_dashboard')
    else:
        initial = {}
        if lapangan_terpilih:
            initial['lapangan'] = lapangan_terpilih
        form = BookingForm(initial=initial)

    # Kirim range jam 0-23 ke template
    jam_range = list(range(24))

    return render(request, 'booking/booking_form.html', {
        'form': form,
        'lapangan_terpilih': lapangan_terpilih,
        'jam_range': jam_range
    })




# ✏️ Update Booking
@login_required
def update_booking_view(request, pk):
    """Mengedit booking tertentu"""
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

        elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = BookingForm(instance=booking)

    return render(request, 'booking/booking_form.html', {'form': form})


# ❌ Batalkan Booking
@login_required
def cancel_booking_view(request, pk):
    """Membatalkan booking"""
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
    """Menampilkan semua booking milik user"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/booking_user_list.html', {'bookings': bookings})

