from django.shortcuts import render

from products.models import Product


def index(request):
    """View function for home page of site."""
    context = {
        "mens": Product.objects.filter(category__name="men").values(
            "name", "description", "price"
        )[:4],
        "womens": Product.objects.filter(category__name="women").values(
            "name", "description", "price"
        )[:4],
        "children": Product.objects.filter(category__name="children").values(
            "name", "description", "price"
        )[:4],
    }
    return render(request, template_name="core/home.html", context=context)
