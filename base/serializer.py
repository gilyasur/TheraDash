from rest_framework import serializers
from .models import Patient, Appointment, TherapistProfile
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView


    
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

# serializers.py in your Django app

from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=30, required=True)
    last_name = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        # Extract first_name and last_name from validated_data
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        # Create user with first_name and last_name
        user = User.objects.create_user(**validated_data, first_name=first_name, last_name=last_name)
        return user

class TherapistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TherapistProfile
        fields = '__all__'