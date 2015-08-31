import autocomplete_light

from .models import Article, SecondaryMenu

autocomplete_light.register(Article, search_fields=['title',])
autocomplete_light.register(SecondaryMenu, search_fields=['name',])
