"""
URL configuration for upload_foto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name="home"),
    path('login/', views.signin, name="login"),
    path('galeria/', views.galeria, name="galeria"),
    path('register/', views.register, name="register"),
    path('', views.index, name="index"),
    path('sair', views.sair, name="sair"),
    path('testes/', views.testes, name="testes"),
    path('excluir_imagem/', views.excluir_imagem, name='excluir_imagem'),
    path('lixeira/', views.lixeira, name='lixeira'),
    path('generate_user_url/', views.generate_user_url, name='generate_user_url'),
    path('save_login_info/', views.save_login_info, name='save_login_info'),
    path('load_login_info/', views.load_login_info, name='load_login_info'),
    path('remember_me/', views.remember_me, name='remember_me'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, )

