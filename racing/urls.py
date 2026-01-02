from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, DriverViewSet, RaceViewSet,RegistrationViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet,basename='team')
router.register(r'drivers', DriverViewSet)
router.register(r'races', RaceViewSet)
router.register(r'Registration',RegistrationViewSet)
 
urlpatterns = [
    path('', include(router.urls)),
]
















# from django.urls import path
# from .views import TeamListCreateView,TeamDetailView

# urlpatterns=[
#     path('teams/', TeamListCreateView.as_view(), name='team-list-create'),
#     path('teams/<int:pk>/', TeamDetailView.as_view(), name='team-detail'),
# ]