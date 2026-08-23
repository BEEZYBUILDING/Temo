from django.urls import path
from . import views

urlpatterns = [
    path('create-intent/', views.CreatePaymentIntentView.as_view(), name='create-intent'),
    path('webhook/', views.StripeWebhookView.as_view(), name='webhook'),
]