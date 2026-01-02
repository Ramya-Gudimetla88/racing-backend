
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone

def validate_dob(value):
    if value > date(2000, 12, 31):
        raise ValidationError("Date of Birth cannot be later than 31/12/2000")

def validate_logo_size(image):
    max_size = 50 * 1024  # 50 KB
    if image.size > max_size:
        raise ValidationError("Logo image size must not exceed 50 KB")

class Team(models.Model):
    team_name = models.CharField(max_length=256, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="logos", validators=[validate_logo_size], null=True, blank=True)
    description = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.team_name

    def delete(self, *args, **kwargs):
        for driver in self.drivers.all():
            # FIX: use registered_races instead of nonexistent 'races'
            if driver.registered_races.exists():
                raise ValidationError("Cannot delete team: one or more drivers are registered in races.")
        super().delete(*args, **kwargs)

class Driver(models.Model):
    first_name = models.CharField(max_length=96)
    last_name = models.CharField(max_length=96)
    dob = models.DateField(validators=[validate_dob])
    registered_races = models.ManyToManyField("Race", related_name="registered_drivers", blank=True)
    team = models.ForeignKey(Team, related_name="drivers", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class RaceQuerySet(models.QuerySet):
    def upcoming(self):
        """Races with race_date in the future (strictly)."""
        today = timezone.now().date()
        return self.filter(race_date__gt=today)

    def completed(self):
        """Races with race_date in the past or today (already happened)."""
        today = timezone.now().date()
        return self.filter(race_date__lte=today)

    
def ordered(self):
        """Useful default ordering: nearest upcoming first, then recent past."""
        today = timezone.now().date()
        # Upcoming first asc, then completed desc
        return self.order_by(
            models.Case(
                models.When(race_date__gt=today, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "race_date",  # within each bucket
        )


class Race(models.Model):
    RaceTrackName = models.CharField(max_length=100)
    trackLocation = models.CharField(max_length=100, null=True, blank=True)
    race_date = models.DateField()
    registration_closure_date = models.DateField(null=True, blank=True)
    objects = RaceQuerySet.as_manager()


    def clean(self):
        if self.race_date <= timezone.now().date():
            raise ValidationError("Race date must be in the future.")
        if self.registration_closure_date and self.registration_closure_date >= timezone.now().date():
            raise ValidationError("Registration closure date must be in the past.")

    def __str__(self):
        return f"{self.RaceTrackName} ({self.trackLocation})"

    # def delete(self, *args, **kwargs):
    #     # FIX: use registered_drivers (related_name) and accurate logic/message
    #     if self.registered_drivers.count() >= 1:
    #         raise ValidationError("Cannot delete race: one or more drivers are registered.")
    #     super().delete(*args, **kwargs)

    
    @property
    def status(self) -> str:
        """Convenient read-only field for serializers/UI."""
        today = timezone.now().date()
        return "upcoming" if self.race_date > today else "completed"




class Registration(models.Model):
    driver=models.ForeignKey(Driver,on_delete=models.CASCADE)
    race=models.ForeignKey(Race,on_delete=models.CASCADE)
    registered_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver}-{self.race}"
