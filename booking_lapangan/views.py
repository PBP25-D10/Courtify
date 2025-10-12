from django.shortcuts import render
from django.http import HttpResponse
from authentication.decorators import role_required, user_required # Impor decorator
from django.contrib.auth.decorators import login_required

@user_required
def booking_dashboard_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'booking/booking_dashboard.html', context)

@login_required
def booking_list_view(request):
    return HttpResponse("Daftar semua lapangan yang bisa dibooking")

@user_required
def booking_create_view(request):
    return HttpResponse("Form booking lapangan")

@user_required
def update_booking_view(request, id):
    return HttpResponse(f"Form update booking ID: {id}")

@user_required
def cancel_booking_view(request, id):
    return HttpResponse(f"Proses cancel booking ID: {id}")