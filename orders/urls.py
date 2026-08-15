from django.urls import path
from . import views

urlpatterns = [
   path('', views.AdminOrderListView.as_view(), name='list'),
   path('checkout/', views.CheckoutView.as_view(), name='checkout'),
   path('<int:pk>/', views.AdminOrderDetailView.as_view(), name='detail'),
   path('<int:pk>/status/', views.AdminOrderStatusView.as_view(), name='status'),
   path('<int:pk>/cancel/', views.OrderCancelView.as_view(), name='cancel'),
   
]