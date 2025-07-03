from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path



router = DefaultRouter()
router.register(r'banks', views.BankViewSet, basename='bank')
router.register(r'devices', views.DeviceViewSet, basename='device')


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard')
]
    

urlpatterns += router.urls
