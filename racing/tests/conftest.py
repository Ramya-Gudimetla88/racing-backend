import pytest
from rest_framework.test import APIClient
from racing.models import Team, Driver, Race, Registration
from datetime import date, timedelta
 
@pytest.fixture
def api_client():
    return APIClient()
 
@pytest.fixture
def team():
    return Team.objects.create(
        team_name="Mercedes",
        city="Brackley",
        country="UK",
        description="F1 Team"
    )
 
@pytest.fixture
def driver(team):
    return Driver.objects.create(
        first_name="Lewis",
        last_name="Hamilton",
        dob="1985-01-07",
        team=team
    )
 
@pytest.fixture
def race():
    return Race.objects.create(
        RaceTrackName="Silverstone",
        trackLocation="UK",
        race_date=date.today() + timedelta(days=10),
        registration_closure_date=date.today() + timedelta(days=5)
    )
 
@pytest.fixture
def registration(driver, race):
    return Registration.objects.create(driver=driver, race=race)
 