from django.test import TestCase
from django.contrib import admin
from racing.admin import Team, Driver, Race
from racing.models import Team as TeamModel, Driver as DriverModel, Race as RaceModel
 
class AdminRegistrationTest(TestCase):
    def test_team_registered_in_admin(self):
        self.assertIn(TeamModel, admin.site._registry)
 
    def test_driver_registered_in_admin(self):
        self.assertIn(DriverModel, admin.site._registry)
 
    def test_race_registered_in_admin(self):
        self.assertIn(RaceModel, admin.site._registry)