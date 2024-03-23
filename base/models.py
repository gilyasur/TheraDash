from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    therapist = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    day_of_week = models.CharField(max_length=10, blank=True, null=True)
    recurring_frequency = models.CharField(max_length=50, blank=True, null=True, default='Weekly')
    canceled = models.BooleanField(default=False, blank=True, null=True)
    cancellation_reason = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Therapist: {self.therapist.username})"


class Appointment(models.Model):
    occurrence_date = models.DateField(default='2024-01-25') 
    therapist = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_of_day = models.TimeField()

    def __str__(self):
        return f"Appointment with {self.patient} ({self.occurrence_date})"

class Transcript(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transcript for {self.appointment}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    title = models.CharField(max_length=100, default='', blank=True)
    address = models.TextField(blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    def __str__(self):
        return self.user.username

    def get_default_title(self):
        return self.user.first_name if self.user.first_name else 'Default Title'