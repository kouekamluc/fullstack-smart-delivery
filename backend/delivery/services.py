import what3words
from django.conf import settings
from .models import Vehicle, Delivery

def assign_delivery_to_vehicle(delivery_id):
    delivery = Delivery.objects.get(id=delivery_id)
    # Logic to find the best vehicle (e.g., closest, available)
    available_vehicles = Vehicle.objects.filter(status='idle')
    if available_vehicles.exists():
        # For simplicity, assign the first available vehicle
        vehicle = available_vehicles.first()
        delivery.vehicle = vehicle
        delivery.status = 'in_transit'
        delivery.save()
        vehicle.status = 'in_transit'
        vehicle.save()
        return vehicle
    return None

def convert_3words_to_coordinates(three_word_address):
    api = what3words.Geocoder(settings.WHAT3WORDS_API_KEY)
    response = api.convert_to_coordinates(three_word_address)
    if 'coordinates' in response:
        return response['coordinates']
    else:
        return None

def convert_coordinates_to_3words(latitude, longitude):
    api = what3words.Geocoder(settings.WHAT3WORDS_API_KEY)
    response = api.convert_to_3wa(latitude=latitude, longitude=longitude)
    if 'words' in response:
        return response['words']
    else:
        return None
