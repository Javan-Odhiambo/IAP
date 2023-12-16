from django.shortcuts import render

# Create your views here.


def homePage(request):
    return render(request, "core/home.html")


def productDetailPage(request, slug):
    return render(request, "core/product-detail.html")


def checkoutPage(request):
    return render(request, "core/checkout.html")


def searchResultsPage(request, slug):
    return render(request, "core/search-results.html")


def categoryPage(request, slug):
    return render(request, "core/category.html")
