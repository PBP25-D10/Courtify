# booking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm


# 🏠 Dashboard Booking
@login_required
def booking_dashboard_view(request):
    """Menampilkan daftar booking milik user yang sedang login"""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/dashboard.html', {'bookings': bookings})


# 📋 List Semua Booking (bisa untuk admin atau penyedia)
@login_required
def booking_list_view(request):
    """Menampilkan semua booking (untuk admin/penyedia)"""
    # Jika admin, tampilkan semua booking; kalau user biasa, tampilkan miliknya
    if request.user.is_staff:
        bookings = Booking.objects.all().order_by('-created_at')
    else:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})


# ➕ Buat Booking Baru
@login_required
def booking_create_view(request):
    """Membuat booking baru"""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # hubungkan ke user yang login
            booking.save()
            messages.success(request, 'Booking berhasil dibuat!')
            return redirect('booking:booking_dashboard')
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
            messages.success(request, 'Booking berhasil diperbarui!')
            return redirect('booking:booking_dashboard')
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
    messages.warning(request, 'Booking telah dibatalkan.')
    return redirect('booking:booking_dashboard')
