"""
URL configuration for DSML_PBL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from DSML_PBL import views
from .token import get_csrf_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home),
    path('result', views.result),
    path('chatp',views.chatpage,name='chatp'),
    path('chat/',views.chat),
    path('accuracy',views.accuracy),
    path('characters',views.characters),
    path('checkgrammar/',views.check_grammer),
    path('score',views.accuracy_score),
    path('clear',views.clear_session),
    path('stopchat', views.stopchat,name='stopchat'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    
]
