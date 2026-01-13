from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import News
from .forms import NewsForm

@login_required
def news_list_view(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.role == 'penyedia':
            news_list = News.objects.all().order_by('-created_at')
            form = NewsForm()
            return render(request, 'artikel/berita_list_owner.html', {'news_list': news_list, 'form': form})
        else:
            return redirect('artikel:news_public_list')
    except:
        return redirect('artikel:news_public_list')

@login_required
def news_create_view(request):
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
