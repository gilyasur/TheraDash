from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from django.contrib.auth.models import User
from .serializer import UserRegistrationSerializer, PatientSerializer, AppointmentSerializer, AppointmentJustSerializer, ProfileSerializer, ProfileDetailSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Patient, Appointment, Profile
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from django.conf import settings
import requests
from django.http import HttpResponse
from django.core.mail import send_mail
import logging
from django.template.loader import render_to_string



logger = logging.getLogger(__name__)


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


class AppointmentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter appointments based on the authenticated user (therapist)
        return Appointment.objects.filter(therapist=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentJustSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        # Set the therapist field when creating an appointment
        serializer.save(therapist=self.request.user)


class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return AppointmentJustSerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        # Filter appointments based on the authenticated user (therapist)
        return Appointment.objects.filter(therapist=self.request.user)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def perform_create(self, serializer):
        # Create a new user
        user = User.objects.create_user(**serializer.validated_data)
        # You may return additional data if needed
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)



@api_view(['PATCH'])
def change_password_view(request, user_id):
    if request.method == 'PATCH':
        # Check if the username is present in the request data
        if 'username' not in request.data:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the user object based on user_id
            user = User.objects.get(pk=user_id)
            # Get the new password and username from the request data
            new_password = request.data.get('new_password')
            username = request.data.get('username')
            
            # Check if the provided username matches the username associated with the user ID
            if username != user.username:
                return Response({'error': 'Username does not match the user ID'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password for the user
            user.set_password(new_password)
            user.save()
            # Optionally, you can update the username as well
            # user.username = username
            # user.save()
            # Return a success response
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Handle case where user with provided user_id does not exist
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # Return an error response for unsupported HTTP methods
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['id'] = user.id
        # Add profile image URL

        try:
            profile = Profile.objects.get(user=user)
            token['profile_image'] = profile.profile_image.url if profile.profile_image else None
        except Profile.DoesNotExist:
            token['profile_image'] = None
        
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



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
    


class ProfileRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'  # Set the lookup field to 'user_id'

    def get_queryset(self):
        # Filter profiles based on the authenticated user
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Assign the current user to the profile being created
        serializer.save(user=self.request.user)

class ProfileListCreateView(APIView):
    def post(self, request, user_id, format=None):
        # Assign the user_id to the user_id field of the profile
        request.data['user_id'] = user_id
        serializer = ProfileSerializer(data=request.data)
        print(user_id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class SendResetPassword(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            
            # Find the user with the given username
            user = User.objects.filter(username=username).first()

            if user is None:
                return Response({'message': 'No user found with this username'}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve the email associated with the user
            email = user.email
            userId=user.id
            
            # Define the email subject and message
            subject = "Password Reset"
            message = f"Dear {user.first_name}, we have just received a password reset request to your account.\n" \
            f"Please follow this link to reset your password: https://example.com/reset-password/{username}/{userId}"

            # Send the email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

            return Response({'message': 'Reset password email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'Failed to send Reset password email: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)