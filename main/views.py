from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect

def landing_page_view(request):
    if request.user.is_authenticated:
        try:
            role = request.user.userprofile.role
            if role == 'penyedia':
                # UBAH INI: Arahkan ke dashboard manajemen
                return redirect('manajemen_lapangan:manajemen_dashboard')
            elif role == 'user':
                # UBAH INI: Arahkan ke dashboard booking
                return redirect('booking_lapangan:booking_dashboard')
            else:
                return redirect('/admin/')
        except AttributeError:
            # Handle jika user tidak punya UserProfile
            return redirect('authentication:login_page') # Asumsi logout dan minta login lagi
    
    # Jika tidak login, tampilkan halaman landing publik
    return render(request, 'main/landing_page.html')

# Views untuk Artikel
def news_list_view(request):
    return HttpResponse("Daftar semua artikel")

def news_create_view(request):
    return HttpResponse("Form tambah artikel (modal)")
# ... view edit & delete artikel

def news_edit_view(request, id):
    pass # 'pass' 

def news_delete_view(request, id):
    pass # 'pass' 

# Views untuk Iklan
def iklan_list_view(request):
    return HttpResponse("Daftar semua iklan")

def iklan_create_view(request):
    return HttpResponse("Form tambah iklan (modal)")
# ... view edit & delete iklan

def iklan_edit_view(request, id):
    pass # 'pass' 

def iklan_delete_view(request, id):
    pass # 'pass' 

# Views untuk Wishlist
def wishlist_list_view(request):
    return HttpResponse("Daftar wishlist user")

def wishlist_create_view(request):
    return HttpResponse("Proses tambah wishlist")
# ... view hapus wishlist

def wishlist_edit_view(request, id):
    pass # 'pass' 

def wishlist_delete_view(request, id):
    pass # 'pass' 