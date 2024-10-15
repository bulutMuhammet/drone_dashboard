from django.urls import path
from .views import PartItemListCreateView, PartItemDetailView, DroneAssemblyView, AssemblyStockCheckView, \
    DroneItemListView, DroneListView, DroneItemDetailView

urlpatterns = [
    path('', DroneListView.as_view(), name="drones-api"),
    path('items/', DroneItemListView.as_view(), name="drone-items-api"),
    path('items/<int:pk>/', DroneItemDetailView.as_view(), name="drone-items-detail-api"),
    path('assemble/', DroneAssemblyView.as_view(), name='assemble-api'),
    path('assembly-stock-check/', AssemblyStockCheckView.as_view(), name='assembly_stock_check-api'),

    path('parts/', PartItemListCreateView.as_view(), name='part-item-list-api'),
    path('parts/<int:pk>/', PartItemDetailView.as_view(), name='part-detail-api'),
]
