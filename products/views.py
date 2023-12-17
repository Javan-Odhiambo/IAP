"""
This module contains view functions for handling product-related requests.
"""

from django.shortcuts import render

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
    query = request.GET.get("q")
    products = models.Product.objects.filter(name__icontains=query)
    context = {
        "products": products,
    }
    return render(request, template_name="core/search-results.html", context=context)


def categories(request):
    """
    View function for displaying categories and their associated products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the category template.
    """
    categories = models.Category.objects.all().prefetch_related("products")
    context = {
        "categories": categories,
    }
    return render(request, template_name="core/category.html", context=context)
