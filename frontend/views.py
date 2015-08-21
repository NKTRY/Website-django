from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from frontend.models import MainMenu, Slider, SecondaryMenu, News, Article, Activity
# Create your views here.


def index(request):
    mains = MainMenu.objects.filter(available=True).order_by("order")
    q = Q(id=-1)
    slider = Slider.objects.order_by("-push__pub_date")[:5]
    if len(slider) == 0:
        slider = None
    news = ()
    for obj in News.category_choice:
        news = news + (News.objects.filter(category=obj[0]).order_by("-push__pub_date")[:7],)
    articles = Article.objects.order_by("-pub_date")[:10]

    try:
        activity = Activity.objects.get(end_date__gte=timezone.now())
    except:
        activity = None
    activities = Activity.objects.order_by("-end_date")[:4]
    if len(activities) != 0:
        if activities[0] == activity:
             activities = activities[1:]
    choices = News.category_choice
    context = {
        "mains": mains,
        "slider": slider,
        "news": news,
        "articles": articles,
        "activity": activity,
        "activities": activities,
        "news_category": choices
    }
    return render(request, "frontend/index.html", context)


def main_menu(request, main):
    main = get_object_or_404(MainMenu, codename=main)
    mains = MainMenu.objects.filter(available=True).order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    context = {
        "main": main,
        "mains": mains,
        "secondaries": secondaries
    }
    return render(request, "frontend/list-main.html", context)


def secondary_menu(request, main, secondary):
    main = get_object_or_404(MainMenu, codename=main)
    secondary = get_object_or_404(SecondaryMenu, codename=secondary)
    mains = MainMenu.objects.filter(available=True).order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    articles = Article.objects.filter(parent=secondary)[:7]
    slider = Slider.objects.filter(category=secondary)
    if len(slider) == 0:
        slider = None
    activity = Activity.objects.filter(category=secondary, end_date__gte=timezone.now())[:1] # TODO: expire
    if len(activity) != 0:
        activity = activity[0]
    else:
        activity = None
    hot = Article.objects.order_by("-hits")[:7]
    context = {
        "main": main,
        "secondary": secondary,
        "mains": mains,
        "secondaries": secondaries,
        "articles": articles,
        "slider": slider,
        "activity": activity,
        "hot": hot
    }
    return render(request, "frontend/list-secondary.html", context)


def secondary_menu_all(request, main, secondary):
    main = get_object_or_404(MainMenu, codename=main)
    secondary = get_object_or_404(SecondaryMenu, codename=secondary)
    mains = MainMenu.objects.filter(available=True).order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    articles = Article.objects.filter(parent=secondary)
    hot = Article.objects.order_by("-hits")[:7]
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


@csrf_exempt
def search(request):
    if request.method == "POST":
        keyword = request.POST["content"]
        if keyword is None:
            return redirect("index")
        q = Q(title__contains=keyword) | Q(text__contains=keyword) | Q(author__nickname=keyword)
        articles = Article.objects.filter(q).order_by('-pub_date')[:7]
        mains = MainMenu.objects.filter(available=True).order_by("order")
        hot = Article.objects.order_by("-hits")[:7]
        if len(articles) == 0:
            has_result = False
        else:
        	has_result = True
        context = {
            "mains": mains,
            "articles": articles,
            "hot": hot,
            "has_result": has_result
        }
        return render(request, "frontend/search-result.html", context)

    if request.method == "GET":
        return redirect("index")


def content(request, main, secondary, id):
    main = get_object_or_404(MainMenu, codename=main)
    secondary = get_object_or_404(SecondaryMenu, codename=secondary)
    article = get_object_or_404(Article, pk=id)
    article.hit()
    mains = MainMenu.objects.filter(available=True).order_by("order")
    secondaries = SecondaryMenu.objects.filter(parent=main).order_by("order")
    q = Q(id=-1)
    for item in secondaries:
        q = q | Q(parent=item)
    hot = Article.objects.filter(q).order_by("-hits")[:7]
    context = {
        "main": main,
        "secondary": secondary,
        "mains": mains,
        "secondaries": secondaries,
        "article": article,
        "hot": hot
    }
    return render(request, "frontend/content-page.html", context)
