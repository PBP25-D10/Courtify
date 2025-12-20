from datetime import timedelta
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.utils import timezone
from django.db import models
from .models import News
from .forms import NewsForm


def _serialize_news(request, news):
    return {
        "id": news.id_berita,
        "title": news.title,
        "content": news.content,
        "kategori": news.kategori,
        "thumbnail": request.build_absolute_uri(news.thumbnail.url) if news.thumbnail else "",
        "created_at": news.created_at.isoformat(),
        "author": news.author.username if news.author else "",
    }


def _json_error(message, status=400):
    return JsonResponse({"status": "error", "message": message}, status=status)


@login_required
def news_list_view(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.role == 'penyedia':
            news_list = News.objects.all().order_by('-created_at')
            search_query = request.GET.get('q', '')
            date_filter = request.GET.get('date_filter', '')

            if search_query:
                news_list = news_list.filter(
                    models.Q(title__icontains=search_query) | models.Q(kategori__icontains=search_query)
                )

            if date_filter == 'today':
                news_list = news_list.filter(created_at__date=timezone.now().date())
            elif date_filter == 'week':
                week_ago = timezone.now() - timedelta(days=7)
                news_list = news_list.filter(created_at__gte=week_ago)
            elif date_filter == 'older':
                week_ago = timezone.now() - timedelta(days=7)
                news_list = news_list.filter(created_at__lt=week_ago)

            form = NewsForm()
            return render(
                request,
                'artikel/berita_list_owner.html',
                {
                    'news_list': news_list,
                    'form': form,
                    'search_query': search_query,
                    'selected_filter': date_filter
                }
            )
        return redirect('artikel:news_public_list')
    except Exception:
        return redirect('artikel:news_public_list')


@login_required
def news_create_view(request):
    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia':
            return JsonResponse(
                {'success': False, 'errors': {'permission': 'Akses ditolak'}},
                status=403
            )
    except Exception:
        return JsonResponse(
            {'success': False, 'errors': {'permission': 'Profile tidak ditemukan'}},
            status=400
        )

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False}, status=405)


@login_required
def news_update_view(request, pk):
    news = get_object_or_404(News, pk=pk)

    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia' or news.author != request.user:
            return JsonResponse(
                {'success': False, 'errors': {'permission': 'Akses ditolak'}},
                status=403
            )
    except Exception:
        return JsonResponse(
            {'success': False, 'errors': {'permission': 'Profile tidak ditemukan'}},
            status=400
        )

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False}, status=405)


@login_required
def news_delete_view(request, pk):
    news = get_object_or_404(News, pk=pk)

    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia' or news.author != request.user:
            return JsonResponse(
                {'success': False, 'errors': {'permission': 'Akses ditolak'}},
                status=403
            )
    except Exception:
        return JsonResponse(
            {'success': False, 'errors': {'permission': 'Profile tidak ditemukan'}},
            status=400
        )

    news.delete()
    return JsonResponse({'success': True})


def news_public_list_view(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(
        request,
        'artikel/berita_public_list.html',
        {'news_list': news_list}
    )


def news_detail_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(
        request,
        'artikel/berita_detail.html',
        {'news': news}
    )


def news_list_json(request):
    news_list = News.objects.all().order_by('-created_at')
    data = [_serialize_news(request, item) for item in news_list]
    return JsonResponse(data, safe=False)


@csrf_exempt
def create_news_flutter(request):
    if request.method != "POST":
        return _json_error("Invalid method", status=405)

    if not request.user.is_authenticated:
        return _json_error("User not authenticated", status=401)

    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia':
            return _json_error("Bukan penyedia", status=403)
    except Exception:
        return _json_error("User profile tidak ditemukan", status=400)

    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return _json_error("Format JSON tidak valid", status=400)

    title = strip_tags(data.get("title", ""))
    content = strip_tags(data.get("content", ""))
    kategori = data.get("kategori", "Komunitas")

    if not title or not content:
        return _json_error("Judul dan konten wajib diisi", status=400)

    news = News.objects.create(
        title=title,
        content=content,
        kategori=kategori,
        author=request.user,
    )

    return JsonResponse(
        {"status": "success", "id": news.id_berita, "news": _serialize_news(request, news)},
        status=201
    )


@csrf_exempt
def delete_news_flutter(request, id):
    if request.method != "POST":
        return _json_error("Invalid method", status=405)

    if not request.user.is_authenticated:
        return _json_error("User not authenticated", status=401)

    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia':
            return _json_error("Bukan penyedia", status=403)
    except Exception:
        return _json_error("User profile tidak ditemukan", status=400)

    try:
        news = News.objects.get(id_berita=id, author=request.user)
        news.delete()
        return JsonResponse({"status": "success"}, status=200)
    except News.DoesNotExist:
        return _json_error("News not found", status=404)

