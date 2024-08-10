from django.db import models

class Vehicle(models.Model):
    name = models.CharField(max_length=255)
    license_plate = models.CharField(max_length=20)
    gps_device_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)  # e.g., 'idle', 'in_transit', 'maintenance'

    def __str__(self):
        return self.name

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='locations')

    def __str__(self):
        return f"Lat: {self.latitude}, Long: {self.longitude}"

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    delivery_id = models.CharField(max_length=255, unique=True)
    pickup_location = models.ForeignKey(Location, related_name='pickup', on_delete=models.SET_NULL, null=True)
    dropoff_location = models.ForeignKey(Location, related_name='dropoff', on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50)  # e.g., 'pending', 'in_progress', 'completed', 'cancelled'
    scheduled_time = models.DateTimeField()
    completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.delivery_id
