from django.contrib import admin
from tecnews.models import NewModel
from tecnews.models import TagModel
# Register your models here.
admin.site.register(NewModel)
admin.site.register(TagModel)
