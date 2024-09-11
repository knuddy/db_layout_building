from django.urls import path
from layouts import views

urlpatterns = [
    path('', views.render_page, name='index'),
]
