import requests
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main.forms import IklanForm
from main.models import Iklan



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

@login_required
def iklan_delete_view(request, id):
    iklan = get_object_or_404(Iklan, pk=id, host=request.user)
    if request.method == 'POST':
        iklan.delete()
        return JsonResponse({'success': True, 'message': 'Berhasil menghapus iklan!'})
    else:
        return JsonResponse({'success': False, 'error': 'Error'}, status=400)


