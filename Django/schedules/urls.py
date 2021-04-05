from django.urls import path
from . import views

app_name = 'schedules'
urlpatterns = [
    path('', views.intro, name='intro' ),
    path('main', views.index, name='index' ),
    path('main2', views.index2, name='index2' ),
    path('carousel', views.carousel, name='carousel'),
    path('introduce', views.introduce, name='introduce'),
]