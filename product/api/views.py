from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.api.serialize import ProductSerializer, ProductListSerializer
from product.models import Product
from django.db.models import FloatField, F, ExpressionWrapper, Value, DecimalField
from django.db.models.functions import Coalesce, Round

# GET, POST, PUT, PATCH, DELETE
@api_view(["GET"])
def index_view(request):
    # product = Product.objects.all()

    product = Product.objects.annotate(
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

    serializer =  ProductListSerializer(product, many=True)
    print(serializer.data)
    return Response(serializer.data)