from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Wishlist
from lapangan.models import Lapangan


DEFAULT_LAPANGAN_IMAGE = "https://images.pexels.com/photos/17724042/pexels-photo-17724042.jpeg"


def _lapangan_image(lapangan):
    if getattr(lapangan, "url_thumbnail", None):
        return lapangan.url_thumbnail
    if lapangan.foto:
        return lapangan.foto.url
    return DEFAULT_LAPANGAN_IMAGE


def _serialize_wishlist_item(item):
    return {
        'id': item.id,
        'lapangan': {
            'id_lapangan': str(item.lapangan.id_lapangan),
            'nama': item.lapangan.nama,
            'kategori': item.lapangan.kategori,
            'lokasi': item.lapangan.lokasi,
            'harga_per_jam': item.lapangan.harga_per_jam,
            'thumbnail': _lapangan_image(item.lapangan),
        },
        'created_at': item.created_at.isoformat()
    }


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


@csrf_exempt
@login_required
def wishlist_api_list(request):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    items = Wishlist.objects.filter(user=request.user).select_related('lapangan')
    data = [_serialize_wishlist_item(item) for item in items]
    return JsonResponse({'status': 'success', 'wishlist': data})


@csrf_exempt
@login_required
def wishlist_api_toggle(request, lapangan_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
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

    return JsonResponse({'status': 'success', 'added': added, 'message': message})


@csrf_exempt
@login_required
def wishlist_api_delete(request, wishlist_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    wishlist = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist.delete()
    return JsonResponse({'status': 'success', 'message': 'Deleted'})


@csrf_exempt
@login_required
def wishlist_api_check(request, lapangan_id):
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    lapangan = get_object_or_404(Lapangan, id_lapangan=lapangan_id)
    in_wishlist = Wishlist.objects.filter(user=request.user, lapangan=lapangan).exists()
    return JsonResponse({'status': 'success', 'in_wishlist': in_wishlist})
