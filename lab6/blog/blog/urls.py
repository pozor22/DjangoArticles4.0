"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from articles import views
from django.contrib.auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', views.archive, name="home"),
    re_path('article/new/', views.create_post, name="create_post"),
    re_path(r'^article/(?P<article_id>\d+)$', views.get_article, name='get_article'),
    re_path('registration/', views.create_user, name="create_user"),
    re_path('authorization/', views.authorization, name="authorization"),
    re_path('exit/', views.exit, name='exit'),
]
