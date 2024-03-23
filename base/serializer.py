from rest_framework import serializers
from .models import Appointment
from .models import Patient
from .models import Profile

from django.contrib.auth.models import User

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentJustSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    occurrence_date = serializers.DateField(format='%Y-%m-%d')

    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient_name(self, obj):
        return obj.patient.first_name + ' ' + obj.patient.last_name if obj.patient else None


class UserRegistrationSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=255, required=False, allow_blank=True)
    specialization = serializers.CharField(max_length=100, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'bio', 'specialization']

    def create(self, validated_data):
        bio = validated_data.pop('bio', None)
        specialization = validated_data.pop('specialization', None)

        user = User.objects.create_user(**validated_data)

        Patient.objects.create(therapist=user, **validated_data)

        return user

class ProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()  

    class Meta:
        model = Profile
        fields = ['user_id', 'profile_image', 'title']


class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'