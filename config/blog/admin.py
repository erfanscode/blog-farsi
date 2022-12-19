from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib import admin
from .models import Article, Category, IPAddress

# Admin Change Template.
admin.site.site_header = "پنل مدیریت"

# Register your models here.
@admin.action(description='انتشار مقالات انتخاب شده')
def make_published(self, request, queryset):
        updated = queryset.update(status='p')
        self.message_user(request, ngettext(
            '%d مقاله منتشر شد.',
            '%d مقاله منتشر شدند.',
            updated,
        ) % updated, messages.SUCCESS)
    

@admin.action(description='پیش نویش شدن مقالات انتخاب شده')
def make_draft(self, request, queryset):
    updated = queryset.update(status='d')
    self.message_user(request, ngettext(
        '%d مقاله پیش نویس شد.',
        '%d مقاله پیش نویس شدند.',
        updated,
    ) % updated, messages.SUCCESS )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'is_special', 'status', 'category_to_str')
    list_filter = ('publish', 'status', 'author')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    actions = [make_published, make_draft]

    # def category_to_str(self, obj):
    #     return ", ".join([category.title for category in obj.category.active()])
    # category_to_str.short_description = "دسته بندی"

admin.site.register(Article, ArticleAdmin)
admin.site.register(IPAddress)