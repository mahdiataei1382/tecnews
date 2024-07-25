from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient , APIRequestFactory
from .models import TagModel, NewModel
from .serializers import NewsSerializer
class NewsViewTestCase(TestCase):
    def setUP(self):
        self.client = APIClient()
    def test_news_list(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/news_list')
        news = NewModel.objects.all()
        serializer = NewsSerializer(news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_one_tag1(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag1')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag1')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_one_tag2(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag2')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag2')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_one_tag3(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag3')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag3')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_one_tag4(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag4')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag4')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_two_tags12(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag1&tags=Tag2')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag1').filter(Tags__Name__icontains='tag2')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_two_tags13(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag1&tags=Tag3')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag1').filter(Tags__Name__icontains='tag3')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_two_tags14(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag1&tags=Tag4')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag1').filter(Tags__Name__icontains='tag4')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_two_tags23(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag3&tags=Tag2')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag3').filter(Tags__Name__icontains='tag2')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_two_tags24(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag4&tags=Tag2')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag4').filter(Tags__Name__icontains='tag2')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_two_tags34(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag3&tags=Tag4')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag3').filter(Tags__Name__icontains='tag4')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_three_tags123(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag1&tags=Tag2&tags=Tag3')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag1').filter(Tags__Name__icontains='tag2').filter(Tags__Name__icontains='tag3')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_by_three_tags234(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag4&tags=Tag2&tags=Tag3')
        filtered_news = NewModel.objects.filter(Tags__Name__icontains='tag4').filter(Tags__Name__icontains='tag2').filter(Tags__Name__icontains='tag3')
        serializer = NewsSerializer(filtered_news, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_filter_news_with_invalid_tags1(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag20')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # Expecting no news articles
    def test_filter_news_with_invalid_tags2(self):
        response = self.client.get('http://127.0.0.1:8000/tecnews/filter/?tags=Tag20&&tags=Tag1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # Expecting no news articles