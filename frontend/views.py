from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from frontend.models import MainMenu, Slider, SecondaryMenu, News, Article, Activity
# Create your views here.


def index(request):
    mains = MainMenu.objects.order_by("order")
    q = Q(id=-1)
    nktc = MainMenu.objects.filter(codename="nktc")
    nktc = SecondaryMenu.objects.filter(parent=nktc)
    for item in nktc:
        q = q | Q(category=item)
    slider = Slider.objects.order_by("push__pub_date")[:5]
    news = ()
    for obj in News.category_choice:
        news = news + (News.objects.filter(category=obj[0]).order_by("push__pub_date")[:7],)
    articles = Article.objects.order_by("pub_date")[:10]
    activities = Activity.objects.filter(q).filter(end_date__gte=timezone.now())[:4]
    choices = News.category_choice
    if len(activities) != 0:
        activity = activities[0]
    else:
        activity = []
    context = {
        "mains": mains,
        "slider": slider,
        "news": news,
        "articles": articles,
        "activity": activity,
        "activities": activities[1:],
        "news_category": choices
    }
    return render(request, "frontend/index.html", context)


def main_menu(request, main):
    main = MainMenu.objects.get(codename=main)
    mains = MainMenu.objects.order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    q = Q(id=-1)
    for item in secondaries:
        q = q | Q(parent=item)
    article = Article.objects.filter(q)
    articles = ()
    for item in Article.category_choices:
        articles = articles + (article.filter(category=item[0])[:10],)
    context = {
        "main": main,
        "mains": mains,
        "secondaries": secondaries,
        "articles": articles
    }
    return render(request, "frontend/list-main.html", context)


def secondary_menu(request, main, secondary):
    main = MainMenu.objects.get(codename=main)
    secondary = SecondaryMenu.objects.get(codename=secondary)
    mains = MainMenu.objects.order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    articles = ()
    for item in Article.category_choices:
        articles = articles + (Article.objects.filter(category=item[0])[:10],)
    slider = Slider.objects.filter(category=secondary)
    activities = Activity.objects.filter(category=secondary)
    hot = Article.objects.filter(parent=secondary).order_by("hits")[:10]
    context = {
        "main": main,
        "secondary": secondary,
        "mains": mains,
        "secondaries": secondaries,
        "articles": articles,
        "slider": slider,
        "activities": activities,
        "hot": hot
    }
    return render(request, "frontend/list-secondary.html", context)


def secondary_menu_all(request, main, secondary):
    main = MainMenu.objects.get(codename=main)
    secondary = SecondaryMenu.objects.get(codename=secondary)
    mains = MainMenu.objects.order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    articles = Article.objects.filter(parent=secondary)
    hot = Article.objects.order_by("hits")[:10]
    articles = Paginator(articles, 7)
    page = request.GET.get('page')
    try:
        articles = articles.page(page)
    except PageNotAnInteger:
        articles = articles.page(1)
    except EmptyPage:
        articles = articles.page(1)
    context = {
        "main": main,
        "secondary": secondary,
        "mains": mains,
        "articles": articles,
        "hot": hot
    }
    return render(request, "frontend/list-secondary-all.html", context)


@csrf_protect
def search(request):
    if request.method == "POST":
        keyword = request.POST["content"]
        if keyword is None:
            return redirect("index")
        q = Q(title__contains=keyword) | Q(text__contains=keyword) | Q(author__nickname=keyword)
        articles = Article.objects.filter(q).order_by('pub_date')[:7]
        mains = MainMenu.objects.order_by("order")
        hot = Article.objects.order_by("hits")[:7]
        context = {
            "mains": mains,
            "articles": articles,
            "hot": hot
        }
        return render(request, "frontend/search-result.html", context)

    if request.method == "GET":
        return redirect("index")


def content(request, main, secondary, id):
    main = MainMenu.objects.get(codename=main)
    secondary = SecondaryMenu.objects.get(codename=secondary)
    article = Article.objects.get(pk=id)
    article.hit()
    mains = MainMenu.objects.order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    q = Q(id=-1)
    for item in secondaries:
        q = q | Q(parent=item)
    hot = Article.objects.filter(q).order_by("hits")[:7]
    context = {
        "main": main,
        "secondary": secondary,
        "mains": mains,
        "secondaries": secondaries,
        "article": article,
        "hot": hot
    }
    return render(request, "frontend/content-page.html", context)