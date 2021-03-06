from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Product, Customer, OrderProduct


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'title', 'customer_id', 'price', 'description',
                  'quantity', 'location', 'image_path', 'created_at', 'product_type_id',
                  'sold_products')


class MyProducts(ViewSet):

    def list(self, request):

        customer = Customer.objects.get(user_id=request.auth.user.id)
        sellers_products = Product.objects.filter(customer_id=customer.id)

        for product in sellers_products:
            
            order_products = OrderProduct.objects.filter(product_id=product.id)
            
            product.sold_products = len(order_products)

            product.quantity -= product.sold_products


        serializer = ProductSerializer(
            sellers_products, many=True, context={'request': request}
        )

        return Response(serializer.data)