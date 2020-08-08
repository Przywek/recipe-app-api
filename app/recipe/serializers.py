from rest_framework import serializers
from core.models import Tag, Ingriedient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngriedientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient serializer objects"""

    class Meta:
        model = Ingriedient
        fields = ('id', 'name')
        read_only_fields = ('id',)
