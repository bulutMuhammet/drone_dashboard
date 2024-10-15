from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from drone.models import PartItem, DroneItem


# arama filtresi
class PartItemSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return ['part__name', 'drone__name', 'serial_number', 'created_at']



class PartItemFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('part__name', 'part_name'),
            ('created_at', 'created_at'),
            ('serial_number', 'serial_number'),
            ('is_used', 'is_used'),
            ('drone__name', 'drone_name'),
        )
    )

    class Meta:
        model = PartItem
        fields = ['is_used', 'serial_number', 'created_at', 'id', 'part', 'drone']


class DroneItemFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('drone__name', 'drone_name'),
            ('created_at', 'created_at'),
            ('serial_number', 'serial_number'),
        )
    )

    class Meta:
        model = DroneItem
        fields = ['serial_number', 'drone', 'created_at', 'id']

class DroneItemSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return ['drone__name', 'serial_number', 'created_at', 'id']