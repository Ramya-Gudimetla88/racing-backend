import pytest
from datetime import date, timedelta
from racing.models import Driver, Race, Registration
from racing.serializers import RegistrationSerializer
from rest_framework.serializers import ValidationError
 
@pytest.mark.django_db
def test_registration_serializer_valid():
    driver = Driver.objects.create(
        first_name="Fernando",
        last_name="Alonso",
        dob=date(1981, 7, 29)
    )
 
    race = Race.objects.create(
        RaceTrackName="Imola",
        race_date=date.today() + timedelta(days=6)
    )
 
    payload = {"driver": driver.id, "race": race.id}
    serializer = RegistrationSerializer(data=payload)
 
    assert serializer.is_valid(), serializer.errors
    serializer.save()
 
@pytest.mark.django_db
def test_registration_serializer_duplicate_registration_fails():
    driver = Driver.objects.create(
        first_name="Sebastian",
        last_name="Vettel",
        dob=date(1987, 7, 3)
    )
 
    race = Race.objects.create(
        RaceTrackName="Hockenheim",
        race_date=date.today() + timedelta(days=9)
    )
 
    Registration.objects.create(driver=driver, race=race)
 
    serializer = RegistrationSerializer(
        data={"driver": driver.id, "race": race.id}
    )
 
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
 