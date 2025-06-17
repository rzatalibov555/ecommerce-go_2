from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .permissions import IsAuthorAuthenticated  # yuxarıda yazdığımız custom permission

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
# @permission_classes([IsAuthenticatedOrReadOnly])
@permission_classes([IsAuthorAuthenticated])  # indi bu istifadə olunacaq
def product_list_create_view(request):
    if request.method == "GET":
        products = annotate_products()
        serializer =  ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
        
            try:
                author_id = request.session.get("author_id")
                author = Author.objects.get(id=author_id)
            except (Author.DoesNotExist, TypeError):
                return Response({"error": "Author not found in session"}, status=404)

            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "PUT", "PATCH", "DELETE"])
# @permission_classes([IsAuthorAuthenticated])  # indi bu istifadə olunacaq
def product_detail_view(request, id):
    pruduct = get_object_or_404(annotate_products(), id=id)
    
    if request.method == "GET":
        serializer = ProductListSerializer(pruduct)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ["PUT", "PATCH"]:
        partial = request.method == "PATCH"  # True, False

        serializer = ProductUpdateSerializer(pruduct, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            #save olunduqdan sonra melumatlari ekrana cixarsin deye elave olunur
            pruduct = get_object_or_404(annotate_products(), id=id)
            serializer = ProductListSerializer(pruduct)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        pruduct.delete()
        return Response({"message":"Mehsul ugurla silindi!"}, status=status.HTTP_204_NO_CONTENT)






















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

   