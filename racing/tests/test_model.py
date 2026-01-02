import pytest
from django.core.exceptions import ValidationError
from racing.models import Team, Driver, Race
from datetime import date, timedelta
 
@pytest.mark.django_db
def test_team_creation():
    team = Team.objects.create(
        team_name="Red Bulls",
        city="Hyderabad",
        country="India"
    )
    assert str(team) == "Red Bulls"
 
@pytest.mark.django_db
def test_team_delete_without_registered_drivers():
    team = Team.objects.create(team_name="Ferrari", city="Rome", country="Italy")
    team.delete()
    assert Team.objects.count() == 0
 
@pytest.mark.django_db
def test_team_delete_with_registered_driver_raises_error():
    team = Team.objects.create(team_name="Mercedes", city="Berlin", country="Germany")
 
    driver = Driver.objects.create(
        first_name="Lewis",
        last_name="Hamilton",
        dob=date(1990, 1, 1),
        team=team
    )
 
    race = Race.objects.create(
        RaceTrackName="Monza",
        race_date=date.today() + timedelta(days=10)
    )
 
    driver.registered_races.add(race)
 
    with pytest.raises(ValidationError):
        team.delete()



 
@pytest.mark.django_db
def test_driver_creation():
    team = Team.objects.create(team_name="McLaren", city="London", country="UK")
    driver = Driver.objects.create(
        first_name="Lando",
        last_name="Norris",
        dob=date(1998, 11, 13),
        team=team
    )
 
    assert str(driver) == "Lando Norris"
    assert driver.team.team_name == "McLaren"



 
@pytest.mark.django_db
def test_race_creation_valid():
    race = Race.objects.create(
        RaceTrackName="Silverstone",
        race_date=date.today() + timedelta(days=5)
    )
    assert race.status == "upcoming"
 
@pytest.mark.django_db
def test_race_date_in_past_invalid():
    race = Race(
        RaceTrackName="Old Track",
        race_date=date.today() - timedelta(days=1)
    )
    with pytest.raises(ValidationError):
        race.clean()
 
@pytest.mark.django_db
def test_registration_closure_date_invalid():
    race = Race(
        RaceTrackName="Future Track",
        race_date=date.today() + timedelta(days=5),
        registration_closure_date=date.today() + timedelta(days=1)
    )
    with pytest.raises(ValidationError):
        race.clean()
 