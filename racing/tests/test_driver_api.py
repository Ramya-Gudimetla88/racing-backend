from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta
from racing.models import Team, Race, Driver
 
 
class DriverAPITest(APITestCase):
 
    def setUp(self):
        self.team = Team.objects.create(
            team_name="Ferrari",
            city="Maranello",
            country="Italy"
        )
 
        self.race = Race.objects.create(
            RaceTrackName="Italian GP",
            race_date=date.today() + timedelta(days=10)
        )
 
    # ---------------- CREATE ----------------
 
    def test_create_driver_without_race(self):
        url = reverse("driver-list")
        data = {
            "first_name": "Sebastian",
            "last_name": "Vettel",
            "dob": "1987-07-03",
            "team": self.team.id
        }
 
        response = self.client.post(url, data, format="json")
 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)
 
    def test_create_driver_with_race(self):
        url = reverse("driver-list")
        data = {
            "first_name": "Charles",
            "last_name": "Leclerc",
            "dob": "1997-10-16",
            "team": self.team.id,
            "registered_races": [self.race.id]
        }
 
        response = self.client.post(url, data, format="json")
 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)
 
    def test_create_driver_invalid_team(self):
        url = reverse("driver-list")
        data = {
            "first_name": "Invalid",
            "last_name": "Driver",
            "dob": "1990-01-01",
            "team": 9999
        }
 
        response = self.client.post(url, data, format="json")
 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
 
    # ---------------- READ ----------------
 
    def test_list_drivers(self):
        Driver.objects.create(
            first_name="Carlos",
            last_name="Sainz",
            dob="1994-09-01",
            team=self.team
        )
 
        url = reverse("driver-list")
        response = self.client.get(url)
 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
 
    def test_get_driver_detail(self):
        driver = Driver.objects.create(
            first_name="Carlos",
            last_name="Sainz",
            dob="1994-09-01",
            team=self.team
        )
 
        url = reverse("driver-detail", args=[driver.id])
        response = self.client.get(url)
 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Carlos")
 
    # ---------------- DELETE ----------------
 
    def test_delete_driver_with_race_not_allowed(self):
        driver = Driver.objects.create(
            first_name="Carlos",
            last_name="Sainz",
            dob="1994-09-01",
            team=self.team
        )
        driver.registered_races.add(self.race)
 
        url = reverse("driver-detail", args=[driver.id])
        response = self.client.delete(url)
 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Driver.objects.filter(id=driver.id).exists())
 
    def test_delete_driver_without_race_allowed(self):
        driver = Driver.objects.create(
            first_name="Mick",
            last_name="Schumacher",
            dob="1999-03-22",
            team=self.team
        )
 
        url = reverse("driver-detail", args=[driver.id])
        response = self.client.delete(url)
 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Driver.objects.filter(id=driver.id).exists())
