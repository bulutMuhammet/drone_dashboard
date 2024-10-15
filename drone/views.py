from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from accounts.models import Team
from .filters import PartItemSearchFilter, PartItemFilter, DroneItemFilter, DroneItemSearchFilter
from .models import PartItem, DroneItem, Drone, Part
from .paginatons import Pagination
from .permissions import IsOwner, IsAssemblyTeam
from .serializers import PartItemSerializer, DroneItemSerializer, DroneStockSerializer, DroneSerializer
from django.shortcuts import get_object_or_404


class PartItemListCreateView(generics.ListCreateAPIView):
    serializer_class = PartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [PartItemSearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PartItemFilter  # FilterSet sınıfını burada belirtiyoruz

    def get_queryset(self):

        if not self.request.user.staff.team.is_assembler:
            user_team = self.request.user.staff.team
            qs = PartItem.objects.filter(part__team=user_team)
        else:
            qs = PartItem.objects.filter()
        return qs.select_related('part', 'drone').order_by('created_at')

    def perform_create(self, serializer):
        # Sadece kullanıcının takımı için parça oluştur
        serializer.save(part=self.request.user.staff.team.part)


class PartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PartItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = PartItem.objects.all()


class DroneItemListView(generics.ListAPIView):
    serializer_class = DroneItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAssemblyTeam]
    queryset = DroneItem.objects.all()

    pagination_class = Pagination
    filter_backends = [DroneItemSearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DroneItemFilter  #


class DroneItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DroneItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAssemblyTeam]
    queryset = DroneItem.objects.prefetch_related('parts__part')


class DroneListView(generics.ListAPIView):
    serializer_class = DroneSerializer
    queryset = Drone.objects.all()


class DroneAssemblyView(generics.CreateAPIView):
    serializer_class = DroneItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsAssemblyTeam]  # Sadece Montaj Takımı üretebilir

    def perform_create(self, serializer):
        drone_item = serializer.save()

        # Parçaları güncelle
        for part_item in drone_item.parts.all():
            part_item.is_used = True
            part_item.save()

        return drone_item


class AssemblyStockCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DroneStockSerializer

    def get(self, request, *args, **kwargs):

        errors = []

        for drone in Drone.objects.all():
            usable_items = PartItem.objects.filter(drone=drone, is_used=False,
                                                   part__team=request.user.staff.team).values_list('part', flat=True)

            unusable_items = Part.objects.filter(team=request.user.staff.team).exclude(id__in=usable_items)

            if unusable_items.exists():
                errors.append(drone.name)

        return Response({
            "drones": errors,
            "part": request.user.staff.team.part.name
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        drone_id = request.data.get('drone_id')

        if not drone_id:
            return Response({"detail": "Uçak ID'si belirtilmeli."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            drone = Drone.objects.get(id=drone_id)
        except Drone.DoesNotExist:
            return Response({"detail": "Uçak bulunamadı."}, status=status.HTTP_404_NOT_FOUND)

        usable_items = PartItem.objects.filter(drone=drone, is_used=False).values_list('part', flat=True)

        unusable_items = Part.objects.exclude(id__in=usable_items)

        if unusable_items.exists():
            return Response({
                "detail": "Bu drone için bazı parçaların stoğu yok",
                "needed_parts": [item.name for item in unusable_items],
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "detail": "Tüm takımlar gerekli parçalara sahip.",
        }, status=status.HTTP_200_OK)
