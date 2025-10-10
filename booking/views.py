from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Booking
from .forms import BookingForm

def booking_list_view(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})


def booking_create_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.save()
            return JsonResponse({'message': 'Booking berhasil dibuat!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = BookingForm()
    return render(request, 'booking/booking_form.html', {'form': form})


def cancel_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'cancelled'
    booking.save()
    return JsonResponse({'message': 'Booking berhasil dibatalkan.'})


def update_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Booking berhasil diperbarui!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/booking_form.html', {'form': form})
