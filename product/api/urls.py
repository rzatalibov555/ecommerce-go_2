from django.urls import path
from . import views

app_name = "product/api"

urlpatterns = [
    path("index/", views.index_view, name="index"),
    path("detail/<id>", views.product_detail_view, name="detail"),
    path("delete/<id>", views.product_delete_view, name="delete"),
    path("create/", views.product_create_view, name="create"),
]
