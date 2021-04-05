from django.urls import path
from . import views

app_name = 'schedules'
urlpatterns = [
    path('', views.intro, name='intro' ),
    path('main', views.index, name='index' )
]