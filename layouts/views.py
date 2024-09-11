from django.shortcuts import render
from layouts.models import Page


def render_page(request):
    page = Page.objects.get(pk=1)
    return render(request, 'page.html',  {'page': page})