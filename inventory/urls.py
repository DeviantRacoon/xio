from django.urls import path
from .views import EquipmentListView

app_name = 'inventory'

urlpatterns = [
    path('', EquipmentListView.as_view(), name='equipment-list'),
]
