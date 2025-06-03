from django.urls import path
from . import views

app_name = "product/api"

urlpatterns = [
    path("index/", views.index_view, name="index"),
]
