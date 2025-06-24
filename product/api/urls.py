from django.urls import path
from product.api.views import product_list_create_view, product_detail_view, index_view, product_create_view, product_delete_view, product_update_put_view, product_update_patch_view

app_name = "product/api"


urlpatterns = [
    path("products/", product_list_create_view, name="products_list_create"), # "GET", "POST"
    path("products/<int:id>", product_detail_view, name="products_detail"),   # "GET", "PUT", "PATCH", "DELETE"
]




# urlpatterns = [
#     path("index/", index_view, name="index"),
#     path("detail/<id>", product_detail_view, name="detail"),
#     path("delete/<id>", product_delete_view, name="delete"),
#     path("create/", product_create_view, name="create"),

#     path("update_put/<id>", product_update_put_view, name="update_put"),
#     path("update_patch/<id>", product_update_patch_view, name="update_patch"),
# ]
