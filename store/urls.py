from django.contrib import admin
from django.urls import path
from store import views
from store.views import CheckOut

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('<pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('cart', views.Cart.as_view(), name='cart'),
    path('check-out', CheckOut.as_view(), name='checkout'),
    path('store', views.store, name='store'),
]