from django import forms
from django_select2 import *

from .models import News, Article

class NewsPushChoices(AutoModelSelect2Field):
    queryset = Article.objects
    search_fields = ['title__icontains',]

class NewsForm(forms.ModelForm):
    push = NewsPushChoices(required=True)

    class Meta:
        model = News
        fields = ('title', 'url', 'push', 'category')
