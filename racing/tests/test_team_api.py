from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from racing.models import Team, Driver, Race
from datetime import date, timedelta
 
 
class TeamAPITest(APITestCase):
 
    def setUp(self):
        self.team = Team.objects.create(
            team_name="Red Bull",
            city="Milton Keynes",
            country="UK"
        )
 
    def test_create_team(self):
        url = reverse("team-list")
        data = {
            "team_name": "Ferrari",
            "city": "Maranello",
            "country": "Italy"
        }
 
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
 
    def test_get_team_list(self):
        url = reverse("team-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_delete_team_blocked_if_driver_has_race(self):
        driver = Driver.objects.create(
            first_name="Max",
            last_name="Verstappen",
            dob="1997-09-30",
            team=self.team
        )
 
        race = Race.objects.create(
            RaceTrackName="Dutch GP",
            race_date=date.today() + timedelta(days=5)
        )
 
        driver.registered_races.add(race)
 
        url = reverse("team-detail", args=[self.team.id])
        response = self.client.delete(url)
 
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Team.objects.filter(id=self.team.id).exists())
