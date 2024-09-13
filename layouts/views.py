from django.views.generic import DetailView
from layouts.models import Page


class PageView(DetailView):
    model = Page
    template_name = "page.html"