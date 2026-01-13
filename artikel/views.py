from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags

from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import News
from .forms import NewsForm
import json

# =====================================================
# WEB DJANGO (UNTUK OWNER / USER VIA BROWSER)
# =====================================================

@login_required
def news_list_view(request):
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
            return render(
                request,
                'artikel/berita_list_owner.html',
                {'news_list': news_list, 'form': form}
            )
            return render(request, 'artikel/berita_list_owner.html', {
                'news_list': news_list,
                'form': form,
                'search_query': search_query,
                'selected_filter': date_filter
            })
        else:
            return redirect('artikel:news_public_list')
    except:
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
    except:
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
    except:
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
    except:
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


# =====================================================
# API UNTUK FLUTTER (JSON)
# =====================================================

def news_list_json(request):
    news_list = News.objects.all().order_by('-created_at')
    data = []

    for item in news_list:
        data.append({
            "id": item.id_berita,
            "title": item.title,
            "content": item.content,
            "kategori": item.kategori,
            "thumbnail": (
                request.build_absolute_uri(item.thumbnail.url)
                if item.thumbnail else ""
            ),
            "created_at": item.created_at.isoformat(),
            "author": item.author.username if item.author else "",
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def create_news_flutter(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Invalid method"},
            status=405
        )

    # 🔐 WAJIB LOGIN
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "User not authenticated"},
            status=401
        )

    # 🔐 WAJIB ROLE PENYEDIA
    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia':
            return JsonResponse(
                {"status": "error", "message": "Bukan penyedia"},
                status=403
            )
    except:
        return JsonResponse(
            {"status": "error", "message": "User profile tidak ditemukan"},
            status=400
        )

    try:
        data = json.loads(request.body)

        title = strip_tags(data.get("title", ""))
        content = strip_tags(data.get("content", ""))
        kategori = data.get("kategori", "Komunitas")

        if not title or not content:
            return JsonResponse(
                {"status": "error", "message": "Judul dan konten wajib diisi"},
                status=400
            )

        news = News.objects.create(
            title=title,
            content=content,
            kategori=kategori,
            author=request.user,
        )

        return JsonResponse(
            {"status": "success", "id": news.id_berita},
            status=200
        )

    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )


@csrf_exempt
def delete_news_flutter(request, id):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Invalid method"},
            status=405
        )

    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "User not authenticated"},
            status=401
        )

    try:
        user_profile = request.user.userprofile
        if user_profile.role != 'penyedia':
            return JsonResponse(
                {"status": "error", "message": "Bukan penyedia"},
                status=403
            )
    except:
        return JsonResponse(
            {"status": "error", "message": "User profile tidak ditemukan"},
            status=400
        )

    try:
        news = News.objects.get(id_berita=id, author=request.user)
        news.delete()
        return JsonResponse({"status": "success"}, status=200)
    except News.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "News not found"},
            status=404
        )

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.html import strip_tags

# from .models import News
# from .forms import NewsForm
# import json

# # =====================================================
# # WEB DJANGO (UNTUK OWNER / USER DI BROWSER)
# # =====================================================

# @login_required
# def news_list_view(request):
#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role == 'penyedia':
#             news_list = News.objects.all().order_by('-created_at')
#             form = NewsForm()
#             return render(
#                 request,
#                 'artikel/berita_list_owner.html',
#                 {'news_list': news_list, 'form': form}
#             )
#         else:
#             return redirect('artikel:news_public_list')
#     except:
#         return redirect('artikel:news_public_list')


# @login_required
# def news_create_view(request):
#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role != 'penyedia':
#             return JsonResponse({'success': False, 'errors': {'permission': 'Akses ditolak'}})
#     except:
#         return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan'}})

#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             news = form.save(commit=False)
#             news.author = request.user
#             news.save()
#             return JsonResponse({'success': True})
#         return JsonResponse({'success': False, 'errors': form.errors})

#     return JsonResponse({'success': False})


# @login_required
# def news_update_view(request, pk):
#     news = get_object_or_404(News, pk=pk)

#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role != 'penyedia' or news.author != request.user:
#             return JsonResponse({'success': False, 'errors': {'permission': 'Akses ditolak'}})
#     except:
#         return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan'}})

#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES, instance=news)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         return JsonResponse({'success': False, 'errors': form.errors})

#     return JsonResponse({'success': False})


# @login_required
# def news_delete_view(request, pk):
#     news = get_object_or_404(News, pk=pk)

#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role != 'penyedia' or news.author != request.user:
#             return JsonResponse({'success': False, 'errors': {'permission': 'Akses ditolak'}})
#     except:
#         return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan'}})

#     news.delete()
#     return JsonResponse({'success': True})


# def news_public_list_view(request):
#     news_list = News.objects.all().order_by('-created_at')
#     return render(request, 'artikel/berita_public_list.html', {'news_list': news_list})


# def news_detail_view(request, pk):
#     news = get_object_or_404(News, pk=pk)
#     return render(request, 'artikel/berita_detail.html', {'news': news})


# # =====================================================
# # API UNTUK FLUTTER (JSON)
# # =====================================================

# def news_list_json(request):
#     news_list = News.objects.all().order_by('-created_at')
#     data = []

#     for item in news_list:
#         data.append({
#             "id": item.id_berita,
#             "title": item.title,
#             "content": item.content,
#             "kategori": item.kategori,
#             "thumbnail": request.build_absolute_uri(item.thumbnail.url) if item.thumbnail else "",
#             "created_at": item.created_at.isoformat(),
#             "author": item.author.username if item.author else "",
#         })

#     return JsonResponse(data, safe=False)


# @csrf_exempt
# def create_news_flutter(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)

#             news = News.objects.create(
#                 title=strip_tags(data.get("title", "")),
#                 content=strip_tags(data.get("content", "")),
#                 kategori=data.get("kategori", "Komunitas"),
#                 author=request.user if request.user.is_authenticated else None,
#             )

#             return JsonResponse({"status": "success", "id": news.id_berita}, status=200)

#         except Exception as e:
#             return JsonResponse({"status": "error", "message": str(e)}, status=400)

#     return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)


# @csrf_exempt
# def delete_news_flutter(request, id):
#     if request.method == "POST":
#         try:
#             news = News.objects.get(id_berita=id)
#             news.delete()
#             return JsonResponse({"status": "success"}, status=200)
#         except News.DoesNotExist:
#             return JsonResponse({"status": "error", "message": "News not found"}, status=404)

#     return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from .models import News
# from .forms import NewsForm

# @login_required
# def news_list_view(request):
#     # Check user role
#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role == 'penyedia':
#             news_list = News.objects.all().order_by('-created_at')
#             form = NewsForm()
#             return render(request, 'artikel/berita_list_owner.html', {'news_list': news_list, 'form': form})
#         else:
#             # Regular user - redirect to public list
#             return redirect('artikel:news_public_list')
#     except:
#         # If no profile, treat as regular user
#         return redirect('artikel:news_public_list')

# @login_required
# def news_create_view(request):
#     # Check if user is penyedia
#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role != 'penyedia':
#             return JsonResponse({'success': False, 'errors': {'permission': 'Hanya penyedia yang dapat menambah berita.'}})
#     except:
#         return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan.'}})

#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES)
#         if form.is_valid():
#             news = form.save(commit=False)
#             news.author = request.user
#             news.save()
#             return JsonResponse({'success': True})
#         return JsonResponse({'success': False, 'errors': form.errors})
#     return JsonResponse({'success': False})

# @login_required
# def news_update_view(request, pk):
#     news = get_object_or_404(News, pk=pk)

#     # Check if user is penyedia and owns the news
#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role != 'penyedia' or news.author != request.user:
#             return JsonResponse({'success': False, 'errors': {'permission': 'Hanya penyedia yang memiliki berita ini yang dapat mengedit.'}})
#     except:
#         return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan.'}})

#     if request.method == 'POST':
#         form = NewsForm(request.POST, request.FILES, instance=news)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'success': True})
#         return JsonResponse({'success': False, 'errors': form.errors})
#     return JsonResponse({'success': False})

# @login_required
# def news_delete_view(request, pk):
#     news = get_object_or_404(News, pk=pk)

#     # Check if user is penyedia and owns the news
#     try:
#         user_profile = request.user.userprofile
#         if user_profile.role != 'penyedia' or news.author != request.user:
#             return JsonResponse({'success': False, 'errors': {'permission': 'Hanya penyedia yang memiliki berita ini yang dapat menghapus.'}})
#     except:
#         return JsonResponse({'success': False, 'errors': {'permission': 'Profile tidak ditemukan.'}})

#     news.delete()
#     return JsonResponse({'success': True})


# def news_public_list_view(request):
#     news_list = News.objects.all().order_by('-created_at')
#     return render(request, 'artikel/berita_public_list.html', {'news_list': news_list})

# def news_detail_view(request, pk):
#     news = get_object_or_404(News, pk=pk)
#     return render(request, 'artikel/berita_detail.html', {'news': news})

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.html import strip_tags
# from .models import News
# import json

# def news_list_json(request):
#     news_list = News.objects.all().order_by('-created_at')
#     data = []

#     for item in news_list:
#         thumbnail_url = (
#             request.build_absolute_uri(item.thumbnail.url)
#             if item.thumbnail
#             else ""
#         )

#         data.append({
#             "id": item.id_berita,
#             "title": item.title,
#             "content": item.content,
#             "kategori": item.kategori,
#             "thumbnail": thumbnail_url,
#             "created_at": item.created_at.isoformat(),
#             "author": item.author.username if item.author else "",
#         })

#     return JsonResponse(data, safe=False)


# @csrf_exempt
# def create_news_flutter(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)

#             title = strip_tags(data.get("title", ""))
#             content = strip_tags(data.get("content", ""))
#             kategori = data.get("kategori", "Komunitas")

#             news = News.objects.create(
#                 title=title,
#                 content=content,
#                 kategori=kategori,
#                 author=request.user if request.user.is_authenticated else None,
#             )

#             return JsonResponse({
#                 "status": "success",
#                 "id": news.id_berita
#             }, status=200)
#         except Exception as e:
#             return JsonResponse({
#                 "status": "error",
#                 "message": str(e),
#             }, status=400)

#     return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

# @csrf_exempt
# def delete_news_flutter(request, id):
#     if request.method == "POST":
#         try:
#             news = News.objects.get(id_berita=id)
#             news.delete()
#             return JsonResponse({"status": "success"}, status=200)
#         except News.DoesNotExist:
#             return JsonResponse({"status": "error", "message": "News not found"}, status=404)
#     return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)
