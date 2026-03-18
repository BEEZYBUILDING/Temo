from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='product'),
    path('<int:pk>/', views.ProductView.as_view(), name='product_id'),
    path('<int:pk>/variants/', views.VariantView.as_view(), name='variant'),
    path('<int:pk>/variants/<int:variant_id>/', views.VariantView.as_view(), name='variant_id'),
    path('<int:pk>/images/', views.ProductImageView.as_view(), name='image')
]