from django.urls import path
from . import views

urlpatterns = [
   path('', views.CartView.as_view(), name='token'),
   path('items/<int:variant_id>/', views.CartItemView.as_view(), name='item'),
   path('validate/', views.CartValidateView.as_view(), name='validate'),
]