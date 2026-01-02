
# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import Registration
from rest_framework.exceptions import ValidationError
from .models import Team, Driver, Race
from .serializers import TeamSerializer, DriverSerializer, RaceSerializer,RegistrationSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        team = self.get_object()
        # FIX: 'drivers' related_name and 'registered_races' M2M
        for driver in team.drivers.all():
            if driver.registered_races.exists():
                return Response(
                    {"error": "Team cannot be deleted: a driver has participated in a race"},
                    status=status.HTTP_204_NO_CONTENT
                )
        return super().destroy(request, *args, **kwargs)


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def get_queryset(self):
        queryset = Driver.objects.all()
        team_id = self.request.query_params.get("team")
        if team_id:
            queryset = queryset.filter(team_id=team_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        driver = self.get_object()
        # Simplify: block delete if ANY registered races exist
        if driver.registered_races.exists():
            return Response(
                {"error": "Cannot delete driver registered for races"},
                status=status.HTTP_204_NO_CONTENT
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def remove_race(self, request, pk=None):
        driver = self.get_object()
        race_id = request.data.get('race_id')

        # Ensure we work with an int id; ignore bad inputs gracefully
        try:
            race_id_int = int(race_id)
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid race_id"},
                status=status.HTTP_204_NO_CONTENT
            )

        if driver.registered_races.count() <= 1:
            return Response(
                {"error": "Driver must have at least one race."},
                status=status.HTTP_204_NO_CONTENT
                
            )

        # Remove (DRF will ignore if not actually related)
        driver.registered_races.remove(race_id_int)
        return Response({"status": "Race removed"})


class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

def destroy(self, request, *args, **kwargs):
        race = self.get_object()
 
        # check if drivers are registered
        if race.drivers.exists():
            return Response(
                {"error": "Cannot delete race: one or more drivers are registered"},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        race.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
def get_queryset(self):
        qs = Race.objects.all()
        status_param = self.request.query_params.get("status", "").lower()
        if status_param == "upcoming":
            qs = qs.upcoming()
        elif status_param == "completed":
            qs = qs.completed()
        return qs.ordered()

class RegistrationViewSet(ModelViewSet):
    queryset=Registration.objects.all()
    serializer_class=RegistrationSerializer
    permission_classes=[AllowAny]
