from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect

from main.forms import IklanForm
from main.models import Iklan

def landing_page_view(request):
    if request.user.is_authenticated:
        try:
            role = request.user.userprofile.role
            if role == 'penyedia':
                # UBAH INI: Arahkan ke dashboard manajemen
                return redirect('manajemen_lapangan:manajemen_dashboard')
            elif role == 'user':
                # UBAH INI: Arahkan ke dashboard booking
                return redirect('booking:booking_dashboard')
            else:
                return redirect('/admin/')
        except AttributeError:
            # Handle jika user tidak punya UserProfile
            return redirect('authentication:login') # Asumsi logout dan minta login lagi
    
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
    iklans = Iklan.objects.filter(host=request.user)
    return render(request, 'iklan_list_owner.html', {'iklans': iklans})

def iklan_create_view(request):
    if request.method == 'POST':
        form = IklanForm(request.POST, request.FILES)
        if form.is_valid():
            iklan_entry = form.save(commit = False)
            iklan_entry.host = request.user
            iklan_entry.save()
            return JsonResponse({'message': 'Iklan dibuat!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = IklanForm()

    return render(request, 'iklan_form.html', {'form': form})

def iklan_edit_view(request, id):
    iklans = get_object_or_404(Iklan, pk=id, host=request.user)
    if request.method == 'POST':
        form = IklanForm(request.POST, request.FILES, instance=iklans)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Berhasil edit iklan!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)    
    else:
      form = IklanForm(instance=iklans)
    return render(request, 'iklan_form.html', {'form': form})

def iklan_delete_view(request, id):
    iklan = get_object_or_404(Iklan, pk=id, host=request.user)
    if request.method == 'POST':
        iklan.delete()
        return JsonResponse({'message': 'Berhasil menghapus iklan!'})
    else:
        return JsonResponse({'error': 'Error'}, status=400)

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