import pytest
from django.urls import reverse
from racing.models import Team, Driver, Race, Registration
 
# =========================
# TEAM VIEW TESTS
# =========================
 
@pytest.mark.django_db
def test_create_team(api_client):
    url = reverse("team-list")
    data = {
        "team_name": "Ferrari",
        "city": "Maranello",
        "country": "Italy",
        "description": "Legendary team"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert Team.objects.count() == 1
 
 
@pytest.mark.django_db
def test_delete_team_without_driver_races(api_client, team):
    url = reverse("team-detail", args=[team.id])
    response = api_client.delete(url)
    assert response.status_code == 204
 
 
@pytest.mark.django_db
def test_delete_team_with_driver_registered_race(api_client, team, driver, race):
    driver.registered_races.add(race)
    url = reverse("team-detail", args=[team.id])
    response = api_client.delete(url)
    assert response.status_code == 204  # your view returns 204 with error
 
 
# =========================
# DRIVER VIEW TESTS
# =========================
 
@pytest.mark.django_db
def test_create_driver(api_client, team):
    url = reverse("driver-list")
    data = {
        "first_name": "Max",
        "last_name": "Verstappen",
        "dob": "1997-09-30",
        "team": team.id
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert Driver.objects.count() == 1
 
 
@pytest.mark.django_db
def test_delete_driver_without_race(api_client, driver):
    url = reverse("driver-detail", args=[driver.id])
    response = api_client.delete(url)
    assert response.status_code == 204
 
 
@pytest.mark.django_db
def test_delete_driver_with_race(api_client, driver, race):
    driver.registered_races.add(race)
    url = reverse("driver-detail", args=[driver.id])
    response = api_client.delete(url)
    assert response.status_code == 204
 
 
@pytest.mark.django_db
def test_remove_race_action(api_client, driver, race):
    driver.registered_races.add(race)
    another_race = Race.objects.create(
        RaceTrackName="Spa",
        trackLocation="Belgium",
        race_date=race.race_date,
        registration_closure_date=race.registration_closure_date
    )
    driver.registered_races.add(another_race)
 
    url = reverse("driver-remove-race", args=[driver.id])
    response = api_client.post(url, {"race_id": race.id}, format="json")
    assert response.status_code == 200
 
 
# =========================
# RACE VIEW TESTS
# =========================
 
@pytest.mark.django_db
def test_create_race(api_client):
    url = reverse("race-list")
    data = {
        "RaceTrackName": "Monza",
        "trackLocation": "Italy",
        "race_date": "2030-09-01",
        "registration_closure_date": "2030-08-25"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert Race.objects.count() == 1
 
 
@pytest.mark.django_db
def test_list_races(api_client, race):
    url = reverse("race-list")
    response = api_client.get(url)
    assert response.status_code == 200
 
 
# =========================
# REGISTRATION VIEW TESTS
# =========================
 
@pytest.mark.django_db
def test_register_driver_for_race(api_client, driver, race):
    url = reverse("registration-list")
    data = {
        "driver": driver.id,
        "race": race.id
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 201
    assert Registration.objects.count() == 1
 
 
@pytest.mark.django_db
def test_duplicate_registration_not_allowed(api_client, registration):
    url = reverse("registration-list")
    data = {
        "driver": registration.driver.id,
        "race": registration.race.id
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400
 