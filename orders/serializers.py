
from rest_framework import serializers
from .models import Order, OrderItem
from core.serializers import ProductSerializer
from core.models import Product
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = OrderItem
        fields = ('id','product','quantity','unit_price','subtotal')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id','customer','seller','items','amount','created_at','updated_at')

    def validate(self, data):
        # Ensure amount matches items
        items = data.get('items', [])
        total = 0
        for it in items:
            total += float(it.get('quantity',1)) * float(it.get('unit_price',0))
        if 'amount' in data and float(data['amount']) != float(total) and float(data.get('amount',0)) != 0:
            raise serializers.ValidationError("Order amount must match sum of items.")
        return data

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            order_items = []
            for it in items:
                prod = it['product']
                oi = OrderItem(order=order, product=prod, quantity=it.get('quantity',1), unit_price=it.get('unit_price', prod.amount))
                oi.save()
                order_items.append(oi)
            order.recalc_amount()
            return order

    def update(self, instance, validated_data):
        items = validated_data.pop('items', None)
        with transaction.atomic():
            for attr, val in validated_data.items():
                setattr(instance, attr, val)
            instance.save()
            if items is not None:
                instance.items.all().delete()
                for it in items:
                    prod = it['product']
                    oi = OrderItem(order=instance, product=prod, quantity=it.get('quantity',1), unit_price=it.get('unit_price', prod.amount))
                    oi.save()
                instance.recalc_amount()
            return instance
