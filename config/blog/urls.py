from django.urls import path
from .views import (
                        ArticleListView,
                        ArticleDetailView,
                        ArticlePreview,
                        CategoryListView,
                        AuthorListView,
                        SearchList,
                    )

app_name = "blog"
urlpatterns = [
    path('', ArticleListView.as_view(), name="home"),
    path('page/<int:page>', ArticleListView.as_view(), name="home"),
    # path('api', api, name="api")
    path('article/<slug:slug>', ArticleDetailView.as_view(), name="detail"),
    path('preview/<int:pk>', ArticlePreview.as_view(), name="preview"),
    path('category/<slug:slug>', CategoryListView.as_view(), name="category"),
    path('category/<slug:slug>/page/<int:page>', CategoryListView.as_view(), name="category"),
    path('author/<slug:username>', AuthorListView.as_view(), name="author"),
    path('author/<slug:username>/page/<int:page>', AuthorListView.as_view(), name="author"),
    path('search/', SearchList.as_view(), name="search"),
    path('search/page/<int:page>', SearchList.as_view(), name="search"),
]   