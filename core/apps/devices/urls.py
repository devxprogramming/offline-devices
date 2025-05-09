from django.urls import path, include
from apps.devices import views



urlpatterns = [
    # Banks
    path('add-bank/', views.AddBank.as_view(), name='add_bank'),
    path('list-banks/', views.ListBanks.as_view(), name='list_banks'),
    path('update-bank/<int:pk>', views.UpdateBank.as_view(), name='update_bank'),
    path('delete-bank/<int:pk>', views.DeleteBank.as_view(), name='delete_bank'),


    # Devices
    path('add-device/', views.AddDevice.as_view(), name='add_device'),
    path('list-devices/', views.ListDevices.as_view(), name='list_devices'),
    path('update-device/<int:pk>', views.UpdateDevice.as_view(), name='update_device'),
    path('delete-device/<int:pk>', views.DeleteDevice.as_view(), name='delete_device'),
]

