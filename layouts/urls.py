from django.urls import path
from layouts import views

urlpatterns = [
    path('<slug:slug>', views.PageView.as_view(), name='index'),
]
