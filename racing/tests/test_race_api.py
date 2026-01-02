from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from racing.models import Race, Driver, Team
from datetime import date, timedelta
 
 
class RaceAPITest(APITestCase):
 
    def test_create_race(self):
        url = reverse("race-list")
        data = {
            "RaceTrackName": "Monaco GP",
            "trackLocation": "Monaco",
            "race_date": date.today() + timedelta(days=20),
            "registration_closure_date": date.today() + timedelta(days=10)
        }
 
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_list_races(self):
        url = reverse("race-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_delete_race_blocked_if_drivers_exist(self):
        team = Team.objects.create(team_name="Alpine", city="Paris", country="France")
 
        driver = Driver.objects.create(
            first_name="Pierre",
            last_name="Gasly",
            dob="1996-02-07",
            team=team
        )
 
        race = Race.objects.create(
            RaceTrackName="French GP",
            race_date=date.today() + timedelta(days=7)
        )
 
        race.registered_drivers.add(driver)
 
        url = reverse("race-detail", args=[race.id])
        response = self.client.delete(url)
 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
 