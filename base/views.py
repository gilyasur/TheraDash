from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from django.contrib.auth.models import User
from .serializer import UserRegistrationSerializer, PatientSerializer, AppointmentSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Patient, Appointment
from rest_framework.response import Response


class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter patients based on the authenticated user (therapist)
        return Patient.objects.filter(therapist=self.request.user)

    def perform_create(self, serializer):
        # Set the therapist to the authenticated user before saving the patient
        serializer.save(therapist=self.request.user)

@permission_classes([IsAuthenticated])
class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def get_queryset(self):
    # Filter patients based on the authenticated user (therapist)
        return Patient.objects.filter(therapist=self.request.user)
    def get_queryset(self):
    # Filter patients based on the authenticated user (therapist)
        return Patient.objects.filter(therapist=self.request.user)


@permission_classes([IsAuthenticated])
class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        # Filter appointments based on the authenticated user (therapist)
        return Appointment.objects.filter(therapist=self.request.user)

    def perform_create(self, serializer):
        # Set the therapist field when creating an appointment
        serializer.save(therapist=self.request.user)


@permission_classes([IsAuthenticated])
class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        # Filter appointments based on the authenticated user (therapist)
        return Appointment.objects.filter(therapist=self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        # Create a new user
        user = User.objects.create_user(**serializer.validated_data)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 
        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email']=user.email
        # ...
 
        return token
 
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class PatientAppointmentListView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer

    def retrieve(self, request, *args, **kwargs):
        # Retrieve the patient based on the patient ID in the URL
        patient = get_object_or_404(Patient, pk=kwargs.get('pk'), therapist=request.user)

        # Filter appointments for the retrieved patient
        appointments = Appointment.objects.filter(patient=patient)
        
        # Serialize and return the data
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)