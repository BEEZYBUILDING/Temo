from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewUpdateDeleteView.as_view(), name='review-update-delete'),
]