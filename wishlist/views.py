from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    return render(request, 'wishlist/wishlist_list.html')
