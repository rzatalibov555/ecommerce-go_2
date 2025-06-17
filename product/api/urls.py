from django.urls import path
from product.api.views import product_list_create_view, product_detail_view

app_name = "product/api"


urlpatterns = [
    path("products/", product_list_create_view, name="products_list_create"), # "GET", "POST"
    path("products/<int:id>", product_detail_view, name="products_detail"),   # "GET", "PUT", "PATCH", "DELETE"

]









# urlpatterns = [
#     path("index/", views.index_view, name="index"),
#     path("detail/<id>", views.product_detail_view, name="detail"),
#     path("delete/<id>", views.product_delete_view, name="delete"),
#     path("create/", views.product_create_view, name="create"),

#     path("update_put/<id>", views.product_update_put_view, name="update_put"),
#     path("update_patch/<id>", views.product_update_patch_view, name="update_patch"),
# ]
