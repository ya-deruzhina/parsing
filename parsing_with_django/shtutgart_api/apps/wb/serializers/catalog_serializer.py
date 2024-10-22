from rest_framework import serializers
from apps.wb.models import ProductModel
        
class CatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields ='__all__'
                
        def create(self, validated_data):
            return ProductModel.objects.get_or_create(**validated_data) 
