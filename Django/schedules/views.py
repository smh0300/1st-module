from django.shortcuts import render
from .models import Article, Job

# Create your views here.



def intro(request):
    return render(request, 'schedules/intro.html')

def index(request):
    articles = Article.objects.all()
    alltime_jobs = Job.objects.filter(end_date='상시채용')
    normal_jobs = Job.objects.exclude(end_date='상시채용')
    context = {'articles':articles, 'alltime_jobs':alltime_jobs, 'normal_jobs':normal_jobs}
    return render(request, 'schedules/index.html',context)