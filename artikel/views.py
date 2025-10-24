from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import News
from .forms import NewsForm

@login_required
def news_list_view(request):
    # Check user role
    try:
        user_profile = request.user.userprofile
        if user_profile.role == 'penyedia':
            news_list = News.objects.all().order_by('-created_at')
            search_query = request.GET.get('q', '')
            date_filter = request.GET.get('date_filter', '')

            # Filter berdasarkan pencarian (judul atau kategori)
            if search_query:
                news_list = news_list.filter(
                    models.Q(title__icontains=search_query) | models.Q(kategori__icontains=search_query)
                )

            # Filter berdasarkan tanggal post
            if date_filter == 'today':
                news_list = news_list.filter(created_at__date=timezone.now().date())
            elif date_filter == 'week':
                week_ago = timezone.now() - timedelta(days=7)
                news_list = news_list.filter(created_at__gte=week_ago)
            elif date_filter == 'older':
                week_ago = timezone.now() - timedelta(days=7)
                news_list = news_list.filter(created_at__lt=week_ago)

            form = NewsForm()
            return render(request, 'artikel/berita_list_owner.html', {
                'news_list': news_list,
                'form': form,
                'search_query': search_query,
                'selected_filter': date_filter
            })
        else:
            # Regular user - redirect to public list
            return redirect('artikel:news_public_list')
    except:
        # If no profile, treat as regular user
        return redirect('artikel:news_public_list')

@login_required
def news_create_view(request):
    # Check if user is penyedia
    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia':
            return JsonResponse({'success': False, 'errors': {'permission': 'Hanya penyedia yang dapat menambah berita.'}})
    except:
        return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan.'}})

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

@login_required
def news_update_view(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Check if user is penyedia and owns the news
    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia' or news.author != request.user:
            return JsonResponse({'success': False, 'errors': {'permission': 'Hanya penyedia yang memiliki berita ini yang dapat mengedit.'}})
    except:
        return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan.'}})

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

@login_required
def news_delete_view(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Check if user is penyedia and owns the news
    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia' or news.author != request.user:
            return JsonResponse({'success': False, 'errors': {'permission': 'Hanya penyedia yang memiliki berita ini yang dapat menghapus.'}})
    except:
        return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan.'}})

    news.delete()
    return JsonResponse({'success': True})


def news_public_list_view(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'artikel/berita_public_list.html', {'news_list': news_list})

def news_detail_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'artikel/berita_detail.html', {'news': news})
