from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'banks', views.BankViewSet, basename='bank')
router.register(r'devices', views.DeviceViewSet, basename='device')


urlpatterns = []

urlpatterns += router.urls