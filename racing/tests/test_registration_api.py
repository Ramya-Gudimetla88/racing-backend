from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from racing.models import Team, Driver, Race, Registration
from datetime import date, timedelta
 
 
class RegistrationAPITest(APITestCase):
 
    def setUp(self):
        self.team = Team.objects.create(
            team_name="Aston Martin",
            city="Silverstone",
            country="UK"
        )
 
        self.driver = Driver.objects.create(
            first_name="Fernando",
            last_name="Alonso",
            dob="1981-07-29",
            team=self.team
        )
 
        self.race = Race.objects.create(
            RaceTrackName="Spanish GP",
            race_date=date.today() + timedelta(days=15)
        )
 
    def test_register_driver_for_race(self):
        url = reverse("registration-list")
        data = {
            "driver": self.driver.id,
            "race": self.race.id
        }
 
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_duplicate_registration_blocked(self):
        Registration.objects.create(driver=self.driver, race=self.race)
 
        url = reverse("registration-list")
        data = {
            "driver": self.driver.id,
            "race": self.race.id
        }
 
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
