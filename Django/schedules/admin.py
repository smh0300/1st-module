from django.contrib import admin
from .models import Article, Job
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display =('id', 'title', 'link', 'time')

admin.site.register(Article, ArticleAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display =('id', 'title', 'link', 'end_date', 'time')

admin.site.register(Job, JobAdmin)