from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Drone, Part, PartItem, DroneItem
from accounts.models import Team


class DroneAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        # Test için gerekli örnek veriler
        self.team = Team.objects.create(name="Kanat Takımı", is_assembler=True)
        self.drone = Drone.objects.create(name="TB2")
        self.part = Part.objects.create(name="Kanat", team=self.team)
        self.part_item = PartItem.objects.create(part=self.part, drone=self.drone)
        self.drone_item = DroneItem.objects.create(drone=self.drone)
        self.drone_item.parts.add(self.part_item)

        self.user = User.objects.create_user(username='testuser@mail.com', email="testuser@mail.com",
                                             password='testpass123')
        self.user.staff.team = self.team
        self.user.staff.save()
        # Kullanıcı için token oluştur
        self.token, created = Token.objects.get_or_create(user=self.user)

        # API client'ı authenticate et
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_drone_list(self):
        url = reverse('drone-items-api')  # Drone listesi için uygun URL'yi ayarlayın
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_drone_detail(self):
        url = reverse('drone-items-detail-api', args=[self.drone.id])  # Drone detay URL'si
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['drone_name'], self.drone.name)

    def test_create_part_item(self):
        url = reverse('part-item-list-api')  # PartItem oluşturma URL'si
        data = {
            "part": self.part.id,
            "drone": self.drone.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
