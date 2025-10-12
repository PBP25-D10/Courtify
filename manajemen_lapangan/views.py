from django.shortcuts import render
from django.http import HttpResponse
from authentication.decorators import role_required, penyedia_required

@penyedia_required
def manajemen_dashboard_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'manajemen_lapangan/manajemen_dashboard.html', context)

@penyedia_required
def lapangan_list_view(request):
    return HttpResponse("Daftar lapangan milik penyedia")

@penyedia_required
def lapangan_create_view(request):
    return HttpResponse("Form tambah lapangan")

@penyedia_required
def lapangan_edit_view(request, id):
    return HttpResponse(f"Form edit lapangan ID: {id}")

@penyedia_required
def lapangan_delete_view(request, id):
    return HttpResponse(f"Proses hapus lapangan ID: {id}")