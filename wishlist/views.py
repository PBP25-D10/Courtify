from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import Wishlist
from lapangan.models import Lapangan


@login_required
def wishlist_list_view(request):
    """Menampilkan daftar wishlist user"""
    wishlists = Wishlist.objects.filter(user=request.user).select_related('lapangan')
    search_query = request.GET.get('q', '')
    kategori_filter = request.GET.get('kategori', '')

    # Filter pencarian nama lapangan
    if search_query:
        wishlists = wishlists.filter(lapangan__nama__icontains=search_query)

    # Filter kategori
    if kategori_filter:
        wishlists = wishlists.filter(lapangan__kategori__iexact=kategori_filter)

    context = {
        'wishlists': wishlists,
        'search_query': search_query,
        'selected_kategori': kategori_filter,
    }
    return render(request, 'wishlist/wishlist_list.html', context)


@login_required
def wishlist_add_view(request, lapangan_id):
    """Menambahkan atau menghapus lapangan dari wishlist"""
    lapangan = get_object_or_404(Lapangan, id_lapangan=lapangan_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, lapangan=lapangan).first()

    if wishlist_item:
        wishlist_item.delete()
        added = False
        message = f"{lapangan.nama} dihapus dari wishlist."
    else:
        Wishlist.objects.create(user=request.user, lapangan=lapangan)
        added = True
        message = f"{lapangan.nama} ditambahkan ke wishlist."

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'added': added, 'message': message})

    messages.success(request, message)
    return redirect('wishlist:wishlist_list')


@login_required
def wishlist_delete_view(request, wishlist_id):
    """Menghapus item wishlist tertentu"""
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    messages.success(request, "Lapangan dihapus dari wishlist.")
    return redirect('wishlist:wishlist_list')


@login_required
def wishlist_check_view(request, lapangan_id):
    """Cek apakah lapangan sudah ada di wishlist user"""
    lapangan = get_object_or_404(Lapangan, id_lapangan=lapangan_id)
    in_wishlist = Wishlist.objects.filter(user=request.user, lapangan=lapangan).exists()
    return JsonResponse({'in_wishlist': in_wishlist})
