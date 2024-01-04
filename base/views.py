from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import generics
# Create your views here.

# views.py

from rest_framework import generics
from .models import Patient
from .serializer import PatientSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
