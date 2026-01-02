import pytest
from racing.models import Team, Driver
from racing.serializers import TeamSerializer
from datetime import date
 
@pytest.mark.django_db
def test_team_serializer_create_with_drivers():
    driver1 = Driver.objects.create(
        first_name="Lando",
        last_name="Norris",
        dob=date(1999, 11, 13)
    )
 
    payload = {
        "team_name": "McLaren",
        "city": "Woking",
        "country": "UK",
        "driver_ids": [driver1.id]
    }
 
    serializer = TeamSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
 
    team = serializer.save()
 
    assert team.drivers.count() == 1
    assert team.drivers.first().first_name == "Lando"
 
@pytest.mark.django_db
def test_team_serializer_driver_ids_read():
    team = Team.objects.create(team_name="Red Bull", city="Milton Keynes", country="UK")
 
    driver = Driver.objects.create(
        first_name="Sergio",
        last_name="Perez",
        dob=date(1990, 1, 26),
        team=team
    )
 
    serializer = TeamSerializer(team)
    assert serializer.data["driver_ids_read"] == [driver.id]


import pytest
from datetime import date, timedelta
from racing.models import Driver, Team, Race
from racing.serializers import DriverSerializer
 
@pytest.mark.django_db
def test_driver_serializer_basic_fields():
    team = Team.objects.create(team_name="Ferrari", city="Rome", country="Italy")
 
    driver = Driver.objects.create(
        first_name="Charles",
        last_name="Leclerc",
        dob=date(1997, 10, 16),
        team=team
    )
 
    serializer = DriverSerializer(driver)
    data = serializer.data
 
    assert data["first_name"] == "Charles"
    assert data["team_name"] == "Ferrari"
    assert data["registered_races_details"] == []
 
@pytest.mark.django_db
def test_driver_serializer_registered_races_details():
    driver = Driver.objects.create(
        first_name="Max",
        last_name="Verstappen",
        dob=date(1997, 9, 30)
    )
 
    race = Race.objects.create(
        RaceTrackName="Monaco",
        race_date=date.today() + timedelta(days=5)
    )
 
    driver.registered_races.add(race)
 
    serializer = DriverSerializer(driver)
    races = serializer.data["registered_races_details"]
 
    assert len(races) == 1
    assert races[0]["RaceTrackName"] == "Monaco"


import pytest
from datetime import date, timedelta
from racing.models import Race, Driver
from racing.serializers import RaceSerializer
 
@pytest.mark.django_db
def test_race_serializer_status_upcoming():
    race = Race.objects.create(
        RaceTrackName="Silverstone",
        race_date=date.today() + timedelta(days=10)
    )
 
    serializer = RaceSerializer(race)
    assert serializer.data["status"] == "upcoming"
 
@pytest.mark.django_db
def test_race_serializer_create_with_drivers():
    driver = Driver.objects.create(
        first_name="George",
        last_name="Russell",
        dob=date(1998, 2, 15)
    )
 
    payload = {
        "RaceTrackName": "Spa",
        "race_date": date.today() + timedelta(days=7),
        "registered_driver_ids": [driver.id]
    }
 
    serializer = RaceSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
 
    race = serializer.save()
    assert race.registered_drivers.count() == 1
 
@pytest.mark.django_db
def test_race_serializer_registered_drivers_count():
    race = Race.objects.create(
        RaceTrackName="Suzuka",
        race_date=date.today() + timedelta(days=8)
    )
 
    serializer = RaceSerializer(race)
    assert serializer.data["registered_drivers_count"] == 0
 