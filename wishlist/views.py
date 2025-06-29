from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import JsonResponse
from .models import Product, Wishlist
from django.contrib.auth.decorators import login_required


@login_required

def wishlist_view(request):
    user = request.user
    wishlisted_items = Wishlist.objects.filter(
        user=user,
        product__isnull=False,
        product__status="available"
    ).select_related('product')  # Optimizes DB queries

    return render(request, 'wishlist/wishlist.html', {
        'wishlisted_items': wishlisted_items
    })

def toggle_wishlist(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

        if not created:
            wishlist_item.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})
    return JsonResponse({'error': 'Invalid request'}, status=400)