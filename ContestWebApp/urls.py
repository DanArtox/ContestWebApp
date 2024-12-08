"""
URL configuration for ContestWebApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
import ContestWebApp.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('success/', views.success),
    path('failure/', views.failure),
    path('', views.contest),
    path('check-participation/', views.CheckParticipation.as_view(), name='check_participation'),
    path('add-user/', views.UserDataBase.as_view(), name='add_user'),
    path('get-users/', views.UserStatsView.as_view(), name='get_users'),
    path('get-ref-chance/', views.GetRefChance.as_view(), name='get_ref_chance'),
    path('success/add-user-chance/', views.AddUserChance.as_view(), name='add_user_chance'),
    path('bot-api/add-user-chance/', views.BotAddUserChance.as_view(), name='bot_add_user_chance'),
    path('bot-api/add-checking-data/', views.BotAddCheckingData.as_view(), name='bot_add_checking_data')
]
