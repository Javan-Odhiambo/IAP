from django.shortcuts import render


# Create your views here.
def product_detail(request, slug):
    return render(request, "core/product-detail.html")


def product_list(request):
    ...


def checkout(request):
    return render(request, "core/checkout.html")


def product_search(request, slug):
    return render(request, "core/search-results.html")


def categories(request, slug):
    return render(request, "core/category.html")
