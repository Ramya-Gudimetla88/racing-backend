from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta
from models import Team, Race, Driver
 
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
 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    