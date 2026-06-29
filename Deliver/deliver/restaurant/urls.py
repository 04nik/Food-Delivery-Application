from django.urls import path
from .views import Dashboard, OrderDetail


urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('order/<int:pk>/', OrderDetail.as_view(), name='order-detail'),
]
