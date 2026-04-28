#from django.urls import path
#from . import views

#urlpatterns = [
#    path('', views.home_page, name='home'),
#    path('product/<int:pk>/', views.product_detail_page, name='product_ui'),
#
#   path('', views.ProductView.as_view(), name='product'),
#    path('<int:pk>/', views.ProductView.as_view(), name='product_id'),
#    path('<int:pk>/variants/', views.VariantView.as_view(), name='variant'),
#    path('<int:pk>/variants/<int:variant_id>/', views.VariantView.as_view(), name='variant_id'),
#    path('<int:pk>/images/', views.ProductImageView.as_view(), name='image'),
  #  path('<int:pk>/detail/', views.ProductDetailView.as_view(), name='product_detail'),
 #   path('api/products/<int:pk>/', views.ProductDetailView.as_view(), name='product_api'),
#]

from django.urls import path
from . import views

urlpatterns = [
    # --- 1. PAGES (HTML for the browser) ---
    path('', views.home_page, name='home'),
    path('product/<int:pk>/', views.product_detail_page, name='product_ui'),

    # --- 2. API (JSON Data for your JavaScript) ---
    # We add 'api/' to the start of these so they don't clash with your pages
    path('api/products/', views.ProductView.as_view(), name='product_list_api'),
    path('api/products/<int:pk>/', views.ProductView.as_view(), name='product_detail_api'),
    path('api/products/<int:pk>/variants/', views.VariantView.as_view(), name='variant'),
    path('api/products/<int:pk>/variants/<int:variant_id>/', views.VariantView.as_view(), name='variant_id'),
    path('api/products/<int:pk>/images/', views.ProductImageView.as_view(), name='image'),
    path('api/products/<int:pk>/detail/', views.ProductDetailView.as_view(), name='product_data_full'),
]