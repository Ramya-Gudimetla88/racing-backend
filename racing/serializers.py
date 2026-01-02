
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Team, Driver, Race,Registration
import json

class DriverSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.team_name", read_only=True)
    registered_races_details = serializers.SerializerMethodField()
    registered_races=serializers.PrimaryKeyRelatedField(many=True,queryset=Race.objects.all(),required=False)

    class Meta:
        model = Driver
        fields = [
            "id",
            "first_name",
            "last_name",
            "dob",
            "registered_races",        
            "team",                    
            "team_name",               
            "registered_races_details" 
        ]

    def get_registered_races_details(self, obj):
        return [
            {
                "id": r.id,
                "RaceTrackName": r.RaceTrackName,
                "location": r.trackLocation,
                "date": r.race_date,
            }
            for r in obj.registered_races.all()
        ]

    def destroy(self, request, *args, **kwargs):
        driver = self.get_object()
        if driver.registered_races.exists():
            return Response(
                {"error": "Cannot delete driver with registered races"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)




class TeamSerializer(serializers.ModelSerializer):
    driver_ids = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source="drivers",  
    )
    drivers = DriverSerializer(many=True, read_only=True)
    driver_ids_read = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "team_name",
            "city",
            "country",
            "description",
            "logo",
            "driver_ids",
            "drivers",
            "driver_ids_read",
        ]

    def get_driver_ids_read(self, obj):
        return list(obj.drivers.values_list("id", flat=True))

    def create(self, validated_data):
        drivers = validated_data.pop("drivers", [])
        team = Team.objects.create(**validated_data)
        if drivers:
            team.drivers.set(drivers)
        return team

    def update(self, instance, validated_data):
        drivers = validated_data.pop("drivers", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if drivers is not None:
            instance.drivers.set(drivers)
        return instance





class RaceSerializer(serializers.ModelSerializer):
    # write to the reverse M2M via source
    registered_driver_ids = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source="registered_drivers",  # write into reverse relation
    )

    registered_drivers = DriverSerializer(many=True, read_only=True)
    registered_drivers_count = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Race
        fields = [
            "id", "RaceTrackName", "trackLocation", "race_date", "registration_closure_date",
            "registered_driver_ids",   # shows a multi-select in DRF HTML form
            "registered_drivers",
            "registered_drivers_count",
            "status",
        ]

    def get_registered_drivers_count(self, obj):
        return obj.registered_drivers.count()

    def get_status(self, obj):
        from django.utils import timezone
        return "upcoming" if obj.race_date > timezone.now().date() else "completed"

    def create(self, validated_data):
        drivers = validated_data.pop("registered_drivers", [])
        race = Race.objects.create(**validated_data)
        if drivers:
            race.registered_drivers.set(drivers)
        return race

    def update(self, instance, validated_data):
        drivers = validated_data.pop("registered_drivers", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if drivers is not None:
            instance.registered_drivers.set(drivers)
        return instance

  
    def get_status(self,obj):
     return obj.status
  
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'driver', 'race']
 
    def validate(self, data):
        if Registration.objects.filter(
            driver=data['driver'],
            race=data['race']
        ).exists():
            raise serializers.ValidationError({"detail":
                "Driver already registered for this race"
            })
        return data







