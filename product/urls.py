from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("products/add/", views.product_add, name="product_add"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:category_id>/", views.category_products, name="category_products"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register")
]
