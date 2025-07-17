from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # Devices URLs
    path('create-device/', views.CreateDeviceView.as_view(), name="create-device-view"),
    path('list-devices/', views.ListDevicesView.as_view(), name="list-devices-view"),
    # path('delete-device/', views.DeleteDevice.as_view(), name="delete-device-view"),
]


# Exports
urlpatterns += [
    path('branch-based-export/', views.BranchBaseExport.as_view(), name="branch-based-export".replace("-", "_")),
    
]
