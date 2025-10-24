from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from lapangan.models import Lapangan
from .models import Wishlist

@login_required
def wishlist_list_view(request):
    """Halaman wishlist user"""
    wishlists = Wishlist.objects.filter(user=request.user).select_related('lapangan')
    return render(request, 'wishlist/wishlist_list.html', {'wishlists': wishlists})


@login_required
def wishlist_add_view(request, lapangan_id):
    """Menambahkan lapangan ke wishlist"""
    lapangan = get_object_or_404(Lapangan, id_lapangan=lapangan_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, lapangan=lapangan)

    if created:
        messages.success(request, f"{lapangan.nama} ditambahkan ke wishlist!")
    else:
        messages.info(request, f"{lapangan.nama} sudah ada di wishlist.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': created})

    return redirect('wishlist:wishlist_list')


@login_required
def wishlist_delete_view(request, wishlist_id):
    """Menghapus wishlist"""
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist.delete()
    messages.success(request, "Lapangan dihapus dari wishlist.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True})

    return redirect('wishlist:wishlist_list')
