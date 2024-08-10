import random
from django.utils import timezone
from .models import Vehicle, Location

def simulate_gps_data(vehicle_id):
    vehicle = Vehicle.objects.get(id=vehicle_id)
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    Location.objects.create(vehicle=vehicle, latitude=latitude, longitude=longitude, timestamp=timezone.now())
