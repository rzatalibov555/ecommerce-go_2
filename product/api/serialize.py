from rest_framework import serializers

from product.models import Product


# Custom Serialize
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    poster = serializers.CharField()
    price = serializers.FloatField()




#Model Serialize
class ProductListSerializer(serializers.ModelSerializer):

    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model  = Product
        fields = '__all__'
        # exclude = ("created_at", "updated_at") 
