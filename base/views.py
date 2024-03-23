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
from .forms import ProfileForm
from datetime import datetime
import logging




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
class CancelPatientStatusView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(canceled=request.data.get('canceled', instance.canceled))
        return Response(serializer.data)

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
        logger = logging.getLogger(__name__)
        logger.info("Generating token for user: %s", user.username)

        token = super().get_token(user)

        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['id'] = user.id

        try:
            profile = Profile.objects.get(user=user)
            token['profile_image'] = profile.profile_image.url if profile.profile_image else None
            token['dob'] = profile.dob.isoformat() if profile.dob else None  
            token['address'] = profile.address if profile.address else None
        except Profile.DoesNotExist:
            token['profile_image'] = None
            
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.info("Token obtain request received")

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            logger.info("Token obtained successfully for user: %s", request.data.get('username'))
        else:
            logger.error("Failed to obtain token for user: %s", request.data.get('username'))

        return response

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
    lookup_field = 'user_id'  

    def get_queryset(self):
        # Filter profiles based on the authenticated user
        return Profile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProfileListCreateView(APIView):
    def post(self, request, user_id, format=None):
        request.data['user_id'] = user_id
        serializer = ProfileSerializer(data=request.data)
        print(user_id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile if hasattr(request.user, 'profile') else None
        form = ProfileForm(instance=profile)
        return Response({'form': form})

    def patch(self, request):
        profile = request.user.profile if hasattr(request.user, 'profile') else None
        form = ProfileForm(request.data, request.FILES, instance=profile)
        if form.is_valid():
            profile_instance = form.save(commit=False)
            profile_instance.user = request.user
            profile_instance.save()
            
            serializer = ProfileSerializer(profile_instance)
            
            return Response({'message': 'Profile updated successfully', 'profile': serializer.data}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SendResetPassword(APIView):
    def post(self, request):
        try:
            logger = logging.getLogger(__name__)
            logger.info("Reset password request received")

            username = request.data.get('username')
            
            user = User.objects.filter(username=username).first()

            if user is None:
                logger.warning("No user found with username: %s", username)
                return Response({'message': 'No user found with this username'}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve the email associated with the user
            email = user.email
            userId = user.id
            
            # Define the email subject and message
            subject = "Password Reset"
            message = f"Dear {user.first_name}, we have just received a password reset request to your account.\n" \
            f"Please follow this link to reset your password: https://example.com/reset-password/{username}/{userId}"

            # Send the email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            logger.info("Reset password email sent to %s", email)

            return Response({'message': 'Reset password email sent successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Failed to send Reset password email: %s", str(e))
            return Response({'message': f'Failed to send Reset password email: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
