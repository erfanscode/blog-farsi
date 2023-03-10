from ipaddress import ip_address
from itertools import count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.views import View
from django.views.generic import ListView, DetailView
from account.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from account.mixins import AuthorAccessMixin
# from taggit.models import Tag
# from django.http import HttpResponse, JsonResponse
from .models import Article, Category
from taggit.models import Tag
from django.db.models import Q


class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context

# Create your views here.
# def home(request, page=1):
#     articles_list = Article.objects.published()
#     paginator = Paginator(articles_list, 4)
#     articles = paginator.get_page(page)

#     context = {
#         # "articles": Article.objects.all()
#         # "articles": Article.objects.published(),
#         "articles": articles,
#     }
#     return render(request, "blog/home.html", context)

class ArticleListView(TagMixin, ListView):
    # model = Article
    queryset = Article.objects.published()
    paginate_by = 4
    # template_name = "blog/list.html"


class ArticleTagList(TagMixin, ListView):
    model = Article
    template_name = 'blog/list.html'
    # context_object_name = 'posts'

    def get_queryset(self):
        return Article.objects.filter(tags__slug=self.kwargs.get('tag_slug'))


# def detail(request, slug):
#     context = {
#         # "articles": Article.objects.all()
#         "article": get_object_or_404(Article.objects.published(), slug=slug)
#     }
#     return render(request, "blog/detail.html", context)
class ArticleDetailView(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        
        return article


class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


# def category(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     articles_list = category.articles.published()
#     paginator = Paginator(articles_list, 2)
#     articles = paginator.get_page(page)

#     context = {
#         "category": category,
#         "articles": articles,
#     }
#     return render(request, "blog/category.html", context)
class CategoryListView(ListView):
    paginate_by = 4
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context



class AuthorListView(ListView):
    paginate_by = 4
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context

'''
def home(request):
    context = {
        "articles": [
            {
                "title": "?????????????? ???????? ???????? ???????? ??????????????: ?????????? ???????????? ?????? ?????? ?????????? ??????",
                "description": "?????????? ?????????????? ???????? ???????????? ???????? ???????????? ???????? ??????: ???? ??????????????? ???? ???????? ???? ?? ???????????????? ???????????? ?????? ???????? ?????????? ???? ???? ??????. ?????? ???????? ???????? ...",
                "img": "https://digiato.com/wp-content/uploads/2022/09/yaze6df9AMIA9oeDEbIZ4zOTRCJ-330x200.webp"
            },
            {
                "title": "?????? ????????: ???????? ???????? ???????????????? ???????????? ???????? ?????????? ???????? ???? ???? ?????????? ??????",
                "description": "???????? ????????????????? ?????????? ???????????? ???????? ???????? ???????????? ???????? ???? ???? ???? ???????????? ?????????? ???????? ??????.",
                "img": "https://digiato.com/wp-content/uploads/2022/09/Screenshot-504-330x200.png"
            }
        ]
    }
    return render(request, "blog/home.html", context)
'''


# def api(request):
#     data = {
#         "1": {
#             "title": "???????? ??????????",
#             "id": 1
#             },
#         "2": {
#             "title": "???????? ??????????",
#             "id": 2
#             },
#         "3": {
#             "title": "???????? ???? ??????",
#             "id": 3
#             },
#         "4": {
#             "title": "???????? ????????",
#             "id": 4
#             }
#     }

#     return JsonResponse(data)

class SearchList(ListView):
    model = Article
    paginate_by = 4
    template_name = "blog/search_list.html"

    def get_queryset(self):
        search = self.request.GET.get('q')
        search_vector = SearchVector("description", weight="B") + SearchVector("title", weight="A")
        search_query = SearchQuery(search)
        search_headline = SearchHeadline("title", search_query)
        return (
            Article.objects.annotate(
                query=search_vector,
                rank=SearchRank(search_vector, search_query))
            .annotate(headline=search_headline)
            .filter(rank__gte=0.3).order_by("-rank")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context