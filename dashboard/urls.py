from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.overview, name='overview'),
    path('articles/', views.articles, name='articles'),
    path('compare/', views.compare, name='compare'),
    path('analysis/', views.analysis, name='analysis'),
    path('trends/', views.trends, name='trends'),
    path('settings/', views.settings_view, name='settings'),
    path('profile/', views.profile, name='profile'),
]
