from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import convert_3words_to_coordinates , convert_coordinates_to_3words , assign_delivery_to_vehicle
from .models import Vehicle, Location, Delivery
from .serializers import VehicleSerializer, LocationSerializer, DeliverySerializer
from rest_framework import status


@api_view(['POST'])
def convert_to_coordinates_view(request):
    three_word_address = request.data.get('three_word_address')
    coordinates = convert_3words_to_coordinates(three_word_address)
    if coordinates:
        return Response(coordinates)
    return Response({"error": "Invalid 3-word address"}, status=400)

@api_view(['POST'])
def convert_to_3words_view(request):
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')
    three_word_address = convert_coordinates_to_3words(latitude, longitude)
    if three_word_address:
        return Response({"three_word_address": three_word_address})
    return Response({"error": "Invalid coordinates"}, status=400)




class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=400)
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]



@api_view(['POST'])
def update_vehicle_location(request):
    vehicle_id = request.data.get('vehicle_id')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    try:
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        return Response({"error": "Vehicle not found"}, status=404)

    Location.objects.create(vehicle=vehicle, latitude=latitude, longitude=longitude)

    return Response({"status": "success", "message": "Location updated successfully"})


@api_view(['POST'])
def assign_delivery_view(request):
    delivery_id = request.data.get('delivery_id')
    vehicle = assign_delivery_to_vehicle(delivery_id)
    if vehicle:
        return Response({"status": "success", "vehicle": vehicle.name})
    return Response({"status": "failure", "message": "No available vehicle"}, status=400)