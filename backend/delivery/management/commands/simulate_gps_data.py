from django.core.management.base import BaseCommand
from delivery.utils import simulate_gps_data
from delivery.models import Vehicle

class Command(BaseCommand):
    help = 'Simulates GPS data for vehicles'

    def handle(self, *args, **kwargs):
        for vehicle in Vehicle.objects.all():
            simulate_gps_data(vehicle.id)
