from django.contrib import admin
from django.urls import path
from cinema_store import views

urlpatterns = [
    path('', views.index, name='home'),
    path("film/<int:film_id>", views.film_page, name="film_page"),
    path("session/<int:session_id>", views.session_page, name="session_page"),
    path('buy-tickets/', views.buy_tickets, name='buy_tickets'),
]