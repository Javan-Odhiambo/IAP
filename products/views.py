"""
This module contains view functions for handling product-related requests.
"""

from django.shortcuts import get_object_or_404, render

from products import models


def product_detail(request, slug, pk):
    """
    View function for displaying product details.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the product.
        pk (int): The primary key of the product.

    Returns:
        HttpResponse: The HTTP response object containing the rendered product detail template.
    """
    product = models.Product.objects.get(pk=pk, slug=slug)
    context = {
        "product": product,
    }
    return render(request, template_name="core/product-detail.html", context=context)


def product_list(request):
    """
    View function that returns a list of products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the product list template.
    """
    products = models.Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, template_name="core/search-results.html", context=context)


def product_search(request):
    """
    View function to handle product search.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the search results template.
    """
    query = request.GET.get("query")
    products = models.Product.objects.filter(name__icontains=query)
    context = {
        "products": products,
    }
    return render(request, template_name="core/search-results.html", context=context)


def categories(request, slug):
    """
    View function for displaying products by category.

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the category.

    Returns:
        HttpResponse: The HTTP response object containing the category template.
    """
    categories = get_object_or_404(models.Category, slug=slug)
    context = {
        "products": categories.products.all(),
    }
    return render(request, template_name="core/category.html", context=context)
