from rest_framework import serializers

from accounts.models import Team
from .models import PartItem, DroneItem, PartItem, Drone, Part


class PartItemSerializer(serializers.ModelSerializer):
    part_name = serializers.SerializerMethodField()
    drone_name = serializers.SerializerMethodField()

    class Meta:
        model = PartItem
        fields = ['id', 'part', 'part_name', 'drone', 'drone_name', 'created_at', 'serial_number', 'is_used']
        read_only_fields = ["serial_number", "part", 'is_used']

    def get_part_name(self, obj):
        return obj.part.name  # Part nesnesinin ismini döndür

    def get_drone_name(self, obj):
        return obj.drone.name  # Drone nesnesinin ismini döndür
class DroneStockSerializer(serializers.Serializer):
    drone_id = serializers.IntegerField()

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'

class DroneItemSerializer(serializers.ModelSerializer):
    drone_name = serializers.SerializerMethodField()
    parts_name = serializers.SerializerMethodField()

    class Meta:
        model = DroneItem
        fields = ['id', 'parts', 'drone', 'drone_name', 'created_at', 'serial_number', 'parts_name']
        read_only_fields = ["serial_number"]

    def get_drone_name(self, obj):
        return obj.drone.name  # Drone nesnesinin ismini döndür

    def get_parts_name(self, obj):
        return [
            {
                'serial_number': part_item.serial_number,
                'part_name': part_item.part.name,
                'is_used': part_item.is_used
            }
            for part_item in obj.parts.all()
        ]

    def validate(self, data):
        drone = data.get('drone')
        parts = data.get('parts')
        errors = {}
        teams = [part_item.part.team.id for part_item in parts]

        existing_teams = Team.objects.filter(is_assembler=False)

        missing_teams = []

        for existing_team in existing_teams:
            if existing_team.id not in teams:
                missing_teams.append(existing_team.part.name)

        if missing_teams:
            errors["missing_parts"] = missing_teams



        used_parts = []
        mismatched_parts = []

        for part_item in parts:

            if part_item.is_used:
                used_parts.append(str(part_item))

            if part_item.drone != drone:
                mismatched_parts.append(str(part_item))

        if used_parts:
            errors["already_used"] = used_parts


        if mismatched_parts:
            errors["mismatched_parts"] = mismatched_parts

        if len({part.part.name for part in parts}) < len(parts):
            errors['duplicated'] = "Aynı türden iki parça kullanılamaz"

        if errors:
            raise serializers.ValidationError({
                "detail": "Hatalar mevcut.",
                "errors": errors  # Hataları burada gruplama yaparak döndür
            })

        return data



