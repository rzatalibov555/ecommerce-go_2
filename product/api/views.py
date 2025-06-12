from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

# from product.api.serialize import ProductSerializer, ProductListSerializer, ProductCreateSerializer, ProductUpdateSerializer
from product.api.serialize import (
    ProductListSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer
)

from product.models import Author, Product
from django.db.models import FloatField, F, ExpressionWrapper, Value, DecimalField
from django.db.models.functions import Coalesce, Round

def annotate_products():
    return Product.objects.annotate(
        discount_price=Coalesce('discount', Value(0), output_field=FloatField()),
        coupon_price=Coalesce('coupon', Value(0), output_field=FloatField()),
        tax=Coalesce('tax_price', Value(0), output_field=FloatField()),
        ).annotate(
        total_price=Round(
            ExpressionWrapper(
                (F('price') * (1 - F('discount_price') / 100) - F('coupon_price') + F('tax')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            precision=2
        )
    )

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def product_list_create_view(request):
    if request.method == "GET":
        products = annotate_products()
        serializer =  ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                author = Author.objects.get(username=request.user.username)
            except Author.DoesNotExist:
                return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def product_detail_view(request, id):
    ...



































# GET, POST, PUT, PATCH, DELETE
# ------------------------------------------------------------------------------
# @api_view(["GET"])
# def index_view(request):
#     # product = Product.objects.all()

#     product = Product.objects.annotate(
#         discount_price=Coalesce('discount', Value(0), output_field=FloatField()),
#         coupon_price=Coalesce('coupon', Value(0), output_field=FloatField()),
#         tax=Coalesce('tax_price', Value(0), output_field=FloatField()),
#         ).annotate(
#         total_price=Round(
#             ExpressionWrapper(
#                 (F('price') * (1 - F('discount_price') / 100) - F('coupon_price') + F('tax')),
#                 output_field=DecimalField(max_digits=10, decimal_places=2)
#             ),
#             precision=2
#         )
#     )

#     serializer =  ProductListSerializer(product, many=True)
#     print(serializer.data)
#     return Response(serializer.data)


# @api_view(["GET"])
# def product_detail_view(request, id):

#     # product = Product.objects.all()
    
#     product = Product.objects.annotate(
#         discount_price=Coalesce('discount', Value(0), output_field=FloatField()),
#         coupon_price=Coalesce('coupon', Value(0), output_field=FloatField()),
#         tax=Coalesce('tax_price', Value(0), output_field=FloatField()),
#         ).annotate(
#         total_price=Round(
#             ExpressionWrapper(
#                 (F('price') * (1 - F('discount_price') / 100) - F('coupon_price') + F('tax')),
#                 output_field=DecimalField(max_digits=10, decimal_places=2)
#             ),
#             precision=2
#         )
#     )

#     product = product.get(id=id)
    
#     serializer = ProductListSerializer(product, many=False)

#     return Response(serializer.data)


# @api_view(["POST"])
# def product_create_view(request):
#     serializer = ProductCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()

#     return Response(serializer.data)

# @api_view(["DELETE"])
# def product_delete_view(request, id):
#     product = Product.objects.annotate(
#         discount_price=Coalesce('discount', Value(0), output_field=FloatField()),
#         coupon_price=Coalesce('coupon', Value(0), output_field=FloatField()),
#         tax=Coalesce('tax_price', Value(0), output_field=FloatField()),
#         ).annotate(
#         total_price=Round(
#             ExpressionWrapper(
#                 (F('price') * (1 - F('discount_price') / 100) - F('coupon_price') + F('tax')),
#                 output_field=DecimalField(max_digits=10, decimal_places=2)
#             ),
#             precision=2
#         )
#     )

#     product = product.get(id=id)

#     product.delete()
#     return Response({"Messege":"Product successfully deleted!"})

# ------------------------------------------------------------------------------

# @api_view(["PUT"]) # Butun sutunlari update etmek lazimdir. // partial=True lazim deyil
# def product_update_put_view(request, id):
#     product = get_object_or_404(Product, id=id)
#     serializer = ProductUpdateSerializer(instance=product, data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)

# @api_view(["PATCH"]) # Lazim olan sutunlari update etmek olar. // partial=True olmalidir
# def product_update_patch_view(request, id):
#     product = get_object_or_404(Product, id=id)
#     serializer = ProductUpdateSerializer(instance=product, data=request.data, partial=True)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)
# ------------------------------------------------------------------------------

   