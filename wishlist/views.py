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
    """Toggle lapangan in wishlist (add if not exists, remove if exists)"""
    lapangan = get_object_or_404(Lapangan, id_lapangan=lapangan_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, lapangan=lapangan).first()

    if wishlist_item:
        # Remove from wishlist
        wishlist_item.delete()
        success = True
        message = f"{lapangan.nama} dihapus dari wishlist."
        added = False
    else:
        # Add to wishlist
        Wishlist.objects.create(user=request.user, lapangan=lapangan)
        success = True
        message = f"{lapangan.nama} ditambahkan ke wishlist!"
        added = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': success, 'message': message, 'added': added})

    if added:
        messages.success(request, message)
    else:
        messages.info(request, message)

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

@login_required
def wishlist_check_view(request, lapangan_id):
    """Check if lapangan is in user's wishlist"""
    lapangan = get_object_or_404(Lapangan, id_lapangan=lapangan_id)
    in_wishlist = Wishlist.objects.filter(user=request.user, lapangan=lapangan).exists()

    return JsonResponse({'in_wishlist': in_wishlist})
