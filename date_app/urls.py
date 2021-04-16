from django.urls import path
from . import views

urlpatterns = [
    path('', views.register_page),
    path('register/', views.register),
    path('login/', views.login),
    path('success/', views.success),
    path('logout/', views.logout),
    path('check/', views.validate_login),
    path('add_date/', views.add_date),
    path('create/', views.create, name="create"),
    path('delete/<int:date_id>/', views.delete),
    path('edit/<int:date_id>/', views.edit, name="edit"),
    path('update/<int:date_id>/', views.update, name="update"),
    path('view/<int:date_id>/', views.view),
    path('complete/<int:date_id>/', views.complete),
    path('favorite/<int:date_id>/', views.favorite),
    path('unfavorite/<int:date_id>/', views.unfavorite),
]