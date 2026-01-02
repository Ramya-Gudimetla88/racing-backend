import pytest
from datetime import date, timedelta
from racing.models import Race
 
@pytest.mark.django_db
def test_upcoming_races_queryset():
    future_race = Race.objects.create(
        RaceTrackName="Future Race",
        race_date=date.today() + timedelta(days=3)
    )
 
    past_race = Race.objects.create(
        RaceTrackName="Past Race",
        race_date=date.today()
    )
 
    upcoming = Race.objects.upcoming()
    assert future_race in upcoming
    assert past_race not in upcoming
 
@pytest.mark.django_db
def test_completed_races_queryset():
    past_race = Race.objects.create(
        RaceTrackName="Completed Race",
        race_date=date.today()
    )
 
    completed = Race.objects.completed()
    assert past_race in completed
 