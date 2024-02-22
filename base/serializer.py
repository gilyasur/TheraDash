from rest_framework import serializers
from .models import Appointment
from .models import Patient
from django.contrib.auth.models import User

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    # Define the occurrence_date field with the desired date format
    occurrence_date = serializers.DateField(format='%Y-%m-%d')

    # Use a nested serializer for the patient field
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'

    # Define a method to get the patient's name
    def get_patient_name(self, obj):
        return obj.patient.first_name + ' ' + obj.patient.last_name if obj.patient else None


class UserRegistrationSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=255, required=False, allow_blank=True)
    specialization = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'bio', 'specialization']

    def create(self, validated_data):
        # Extract additional fields from serializer data
        bio = validated_data.pop('bio', None)
        specialization = validated_data.pop('specialization', None)

        # Create user with first_name and last_name
        user = User.objects.create_user(**validated_data)

        # Create a Patient linked to the new user
        Patient.objects.create(therapist=user, **validated_data)

        return user
