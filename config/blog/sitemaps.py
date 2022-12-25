from django.contrib.sitemaps import Sitemap
from .models import Article

class BlogSitemap(Sitemap):
    changefreq  = 'weekly'
    priority    = 0.9  # max=1

    def items(self):
        return Article.objects.filter(status='p')
    
    def lastmod(self, obj):
        return obj.updated