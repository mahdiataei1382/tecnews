from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import NewModel
from .serializers import NewsSerializer
from rest_framework.response import Response

@api_view(["GET"])
def news_list (requset):
    news = NewModel.objects.all()
    news_serialize = NewsSerializer(news , many = True)
    return Response(news_serialize.data)

@api_view(['GET'])
def filter_news_by_tags(request):
    tags = request.GET.getlist('tags')  # Convert provided tags to lowercase
    filtered_news = NewModel.objects.filter(Tags__Name__icontains=tags[0])  # Filter news based on the first tag
    for tag in tags[1:] :
        filtered_news = filtered_news.filter(Tags__Name__icontains=tag)  # Filter news further based on the remaining tags
    news_serialize = NewsSerializer(filtered_news, many=True)
    return Response(news_serialize.data)
