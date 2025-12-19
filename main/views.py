import requests
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.forms import IklanForm
from main.models import Iklan
from django.views.decorators.csrf import csrf_exempt

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)

def landing_page_view(request):
    iklan_list = Iklan.objects.all()[:10]
    if request.user.is_authenticated:
        try:
            role = request.user.userprofile.role
            if role == 'penyedia':
                return render(request, 'main/landing_page.html', {'iklan_list': iklan_list})
            elif role == 'user':
                return render(request, 'main/landing_page.html', {'iklan_list': iklan_list})
            else:   
                return redirect('/admin/')
        except AttributeError:
            # Handle jika user tidak punya UserProfile
            return redirect('authentication:login')
    return render(request, 'main/landing_page.html', {'iklan_list': iklan_list})

def iklan_list_view(request):
    iklans = Iklan.objects.filter(host=request.user).select_related('lapangan')
    search_query = request.GET.get('q', '')  
    date_filter = request.GET.get('date_filter', '')  

    # Filter berdasarkan pencarian (judul atau nama lapangan)
    if search_query:
        iklans = iklans.filter(lapangan__nama__icontains=search_query) | iklans.filter(judul__icontains=search_query)

    # Filter berdasarkan tanggal post
    if date_filter == 'today':
        iklans = iklans.filter(date__date=timezone.now().date())
    elif date_filter == 'week':
        week_ago = timezone.now() - timedelta(days=7)
        iklans = iklans.filter(date__gte=week_ago)
    elif date_filter == 'older':
        week_ago = timezone.now() - timedelta(days=7)
        iklans = iklans.filter(date__lt=week_ago)

    return render(request, 'main/iklan_list_owner.html', {
        'iklan_list': iklans,
        'search_query': search_query,
        'selected_filter': date_filter
    })

@csrf_exempt
@login_required
def iklan_create_view(request):
    if request.method == 'POST':
        form = IklanForm(request.POST or None, request.FILES or None, user=request.user)
        if form.is_valid():
            iklan_entry = form.save(commit = False)
            iklan_entry.host = request.user
            iklan_entry.save()
            return JsonResponse({'success': True, 'message': 'Iklan dibuat!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = IklanForm(user=request.user)

    return render(request, 'main/iklan_form.html', {'form': form})

@csrf_exempt
@login_required
def iklan_edit_view(request, id):
    iklans = get_object_or_404(Iklan, pk=id, host=request.user)
    if request.method == 'POST':
        form = IklanForm(request.POST, request.FILES, instance=iklans)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Berhasil edit iklan!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)    
    else:
      form = IklanForm(instance=iklans)
    return render(request, 'main/iklan_form.html', {'form': form})

@csrf_exempt
@login_required
def iklan_delete_view(request, id):
    iklan = get_object_or_404(Iklan, pk=id, host=request.user)
    if request.method == 'POST':
        iklan.delete()
        return JsonResponse({'success': True, 'message': 'Berhasil menghapus iklan!'})
    else:
        return JsonResponse({'success': False, 'error': 'Error'}, status=400)

@csrf_exempt
def flutter_api_list_iklan(request):
    """API endpoint for Flutter to get list of Iklan for logged-in penyedia"""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    # Check authentication
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    # Check if user is penyedia
    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can access this'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)
    
    # Get iklan for this penyedia
    iklan_list = Iklan.objects.filter(host=request.user).select_related('lapangan')
    
    data = []
    for iklan in iklan_list:
        data.append({
            'pk': iklan.pk,
            'judul': iklan.judul,
            'deskripsi': iklan.deskripsi,
            'banner': iklan.banner.url if iklan.banner else None,
            'tanggal': iklan.date.strftime("%Y-%m-%d"), # Format tanggal string
            'lapangan_id': iklan.lapangan.pk,
            'lapangan_nama': iklan.lapangan.nama, # Tambahan info biar mudah di flutter
        })
    
    return JsonResponse({'status': 'success', 'iklan_list': data})


@csrf_exempt
def flutter_api_landing_page_iklan(request):
    """API endpoint for public landing page ads"""
    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
        
    data_iklan = Iklan.objects.select_related('lapangan').all()[:10]
    
    data = []
    for iklan in data_iklan:
        data.append({
            'pk': iklan.pk,
            'judul': iklan.judul,
            'deskripsi': iklan.deskripsi,
            'banner': iklan.banner.url if iklan.banner else None,
            'tanggal': iklan.date.strftime("%Y-%m-%d"),
            'lapangan_id': iklan.lapangan.pk,
            'lapangan_nama': iklan.lapangan.nama,
        })

    # Menggunakan format wrapper agar konsisten dengan API lainnya
    return JsonResponse({'status': 'success', 'iklan_list': data})


@csrf_exempt
def flutter_api_create_iklan(request):
    """API endpoint for Flutter to create new Iklan"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can create iklan'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)

    try:
        data = request.POST

        # ✅ Handle JSON Payload (jika Flutter mengirim pure JSON tanpa gambar)
        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body.decode('utf-8') or '{}')
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

            # Jika "banner" berupa string path (bukan file), hapus agar tidak error di Form
            if isinstance(payload, dict) and isinstance(payload.get('banner'), str):
                payload.pop('banner', None)

            qd = QueryDict('', mutable=True)
            if isinstance(payload, dict):
                for k, v in payload.items():
                    if v is None: continue
                    qd[k] = str(v)
            data = qd

        # Menggunakan IklanForm untuk validasi
        form = IklanForm(data, request.FILES)
        
        if form.is_valid():
            iklan = form.save(commit=False)
            iklan.host = request.user # Set Host otomatis dari user login
            
            # Validasi kepemilikan lapangan (Penyedia tidak boleh buat iklan untuk lapangan orang lain)
            # Asumsi field form bernama 'lapangan'
            if iklan.lapangan.owner != request.user:
                 return JsonResponse({'status': 'error', 'message': 'Anda tidak bisa membuat iklan untuk lapangan yang bukan milik Anda'}, status=403)

            iklan.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Iklan berhasil dibuat',
                'iklan': {
                    'pk': iklan.pk,
                    'judul': iklan.judul,
                    'deskripsi': iklan.deskripsi,
                    'banner': iklan.banner.url if iklan.banner else None,
                    'lapangan': iklan.lapangan.nama
                }
            })
        else:
             # Extract error messages
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            return JsonResponse({'status': 'error', 'message': '; '.join(error_messages)}, status=400)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Terjadi kesalahan: {str(e)}'}, status=500)


@csrf_exempt
def flutter_api_update_iklan(request, id_iklan):
    """API endpoint for Flutter to update Iklan"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can update iklan'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)

    try:
        iklan = get_object_or_404(Iklan, pk=id_iklan)

        # Check ownership (Pastikan yang edit adalah pembuat iklan)
        if iklan.host != request.user:
            return JsonResponse({'status': 'error', 'message': 'You do not own this iklan'}, status=403)

        data = request.POST

        # ✅ Handle JSON Payload
        if request.content_type and 'application/json' in request.content_type:
            try:
                payload = json.loads(request.body.decode('utf-8') or '{}')
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

            if isinstance(payload, dict) and isinstance(payload.get('banner'), str):
                payload.pop('banner', None)

            qd = QueryDict('', mutable=True)
            if isinstance(payload, dict):
                for k, v in payload.items():
                    if v is None: continue
                    qd[k] = str(v)
            data = qd

        form = IklanForm(data, request.FILES, instance=iklan)
        if form.is_valid():
            updated_iklan = form.save(commit=False)
            
            # Validasi ulang kepemilikan lapangan jika lapangan diubah
            if updated_iklan.lapangan.owner != request.user:
                 return JsonResponse({'status': 'error', 'message': 'Lapangan yang dipilih bukan milik Anda'}, status=403)
            
            updated_iklan.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Iklan berhasil diperbarui',
                'iklan': {
                    'pk': updated_iklan.pk,
                    'judul': updated_iklan.judul,
                }
            })
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            return JsonResponse({'status': 'error', 'message': '; '.join(error_messages)}, status=400)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error: {str(e)}'}, status=500)


@csrf_exempt
def flutter_api_delete_iklan(request, id_iklan):
    """API endpoint for Flutter to delete Iklan"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=401)

    try:
        if request.user.userprofile.role != 'penyedia':
            return JsonResponse({'status': 'error', 'message': 'Only penyedia can delete iklan'}, status=403)
    except AttributeError:
        return JsonResponse({'status': 'error', 'message': 'User profile not found'}, status=403)
    
    try:
        iklan = get_object_or_404(Iklan, pk=id_iklan)
        
        # Check ownership
        if iklan.host != request.user:
            return JsonResponse({'status': 'error', 'message': 'You do not own this iklan'}, status=403)
        
        iklan.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Iklan berhasil dihapus'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error: {str(e)}'
        }, status=500)