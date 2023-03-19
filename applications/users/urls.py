#
from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = "users_app"

urlpatterns = [
    path(
        'login/', 
        views.LoginUser.as_view(),
        name='user-login',
    ),
    path('', lambda request: redirect('login/')),
    path(
        'logout/', 
        views.LogoutView.as_view(),
        name='user-logout',
    ),
    path(
        'database/', 
        views.DatabaseView.as_view(),
        name='user-database',
    ),
    path('database/list/', views.database_list, name='database_list'),
]