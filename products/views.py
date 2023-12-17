from django.shortcuts import render

from products import models


# Create your views here.
def product_detail(request, slug, pk):
    product = models.Product.objects.get(pk=pk, slug=slug)
    context = {
        "product": product,
    }
    return render(request, template_name="core/product-detail.html", context=context)


def product_list(request):
    products = models.Product.objects.all()
    context = {
        "products": products,
    }
    # template unknown
    return render(request, template_name="core/search-results.html", context=context)


def product_search(request):
    query = request.GET.get("q")
    products = models.Product.objects.filter(name__icontains=query)
    context = {
        "products": products,
    }
    return render(request, template_name="core/search-results.html", context=context)


def categories(request):
    categories = models.Category.objects.all().prefetch_related("products")
    context = {
        "categories": categories,
    }
    return render(request, template_name="core/category.html", context=context)
