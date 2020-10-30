from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.StackSearch.as_view(), name="index"),
]