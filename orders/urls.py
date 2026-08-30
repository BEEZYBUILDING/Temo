from django.urls import path
from . import views

urlpatterns = [
   path('', views.AdminOrderListView.as_view(), name='list'),
   path('checkout/', views.CheckoutView.as_view(), name='checkout'),
   path('<int:pk>/', views.AdminOrderDetailView.as_view(), name='detail'),
   path('<int:pk>/status/', views.AdminOrderStatusView.as_view(), name='status'),
   path('<int:pk>/cancel/', views.OrderCancelView.as_view(), name='cancel'),
   path('my/<int:pk>/', views.OrderDetailView.as_view(), name='my-order-detail'),
   path('my/', views.OrderListView.as_view(), name='my-orders'),
   path('coupons/', views.AdminCouponListCreateView.as_view(), name='coupon-list-create'),
   path('coupons/validate/', views.CouponValidateView.as_view(), name='coupon-validate'),
   path('coupons/<int:pk>/', views.AdminCouponUpdateDeleteView.as_view(), name='coupon-update-delete'),
]