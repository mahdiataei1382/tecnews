from rest_framework import serializers
from .models import NewModel, TagModel

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = ['id', 'Name']

class NewsSerializer(serializers.ModelSerializer):
    Tags = TagSerializer(many=True)
    class Meta:
        model = NewModel
        fields = ['id', 'Title', 'Text', 'Tags', 'Source']
