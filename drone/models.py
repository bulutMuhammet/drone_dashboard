import uuid

from django.db import models

from accounts.models import Team


class Drone(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Part(models.Model):
    name = models.CharField(max_length=50)
    team = models.OneToOneField(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PartItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='items')
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    serial_number = models.CharField(max_length=36, default=uuid.uuid4)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.part.name} ({self.drone}) - ( IS USED = {self.is_used}) - {self.serial_number}"

class DroneItem(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name="items")  # Üretilen drone tipi
    created_at = models.DateTimeField(auto_now_add=True)
    serial_number = models.CharField(max_length=36, default=uuid.uuid4)
    parts = models.ManyToManyField(PartItem)

    def __str__(self):
        return f"{self.drone.name} - {self.id}"



