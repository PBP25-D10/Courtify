# booking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Booking
from .models import Lapangan
from .forms import BookingForm

# 🏠 Dashboard Booking
@login_required
def booking_dashboard_view(request):
    """Menampilkan daftar booking milik user yang sedang login"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    # Respons AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(bookings.values())
        return JsonResponse({'bookings': data})

    return render(request, 'booking/dashboard.html', {'bookings': bookings})


# 📋 List Semua Booking (bisa untuk admin atau penyedia)
@login_required
def booking_list_view(request):
    """Menampilkan daftar lapangan agar bisa dipilih untuk booking"""
    lapangan_list = Lapangan.objects.all().order_by('nama')

    return render(request, 'booking/booking_list.html', {
        'lapangan_list': lapangan_list
    })



# ➕ Buat Booking Baru
@login_required
def booking_create_view(request):
    """Membuat booking baru (bisa dengan lapangan yang sudah dipilih)"""
    lapangan_id = request.GET.get('lapangan_id')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Booking berhasil dibuat!')
            return redirect('booking:booking_dashboard')
    else:
        # kalau user datang dari tombol 'Pesan', isi otomatis lapangan
        if lapangan_id:
            form = BookingForm(initial={'lapangan': lapangan_id})
        else:
            form = BookingForm()

    return render(request, 'booking/booking_form.html', {'form': form})



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
