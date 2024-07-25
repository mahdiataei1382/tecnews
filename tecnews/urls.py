from django.urls import path
from .views import news_list
urlpatterns = [
    path ("news_list" , news_list)
]
from django.urls import path
from .views import news_list
from .views import filter_news_by_tags

urlpatterns = [
    path("news_list" , news_list),
    path('filter/', filter_news_by_tags),
]