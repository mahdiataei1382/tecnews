from rest_framework import serializers
from .models import NewModel, TagModel

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['id', 'name']

class NewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = NewModel
        fields = ['id', 'title', 'text', 'tags', 'source']
