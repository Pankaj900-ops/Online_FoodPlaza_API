
from rest_framework import serializers
from .models import Product, PlatformApiCall, Customer, Seller

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','amount','created_at','updated_at')

    def validate_name(self, value):
        # Prevent duplicate products (case-insensitive)
        if Product.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Product with this name already exists.")
        return value

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id','name','mobile','user')

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ('id','name','mobile','user')

class PlatformApiCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformApiCall
        fields = '__all__'
