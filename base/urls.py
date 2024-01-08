from django.urls import path
from .views import PatientListCreateView, PatientRetrieveUpdateDestroyView, AppointmentDetailView,AppointmentListCreateView, UserRegistrationView, TherapistProfileDetailView, TherapistProfileListCreateView
from . import views
urlpatterns = [
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient-retrieve-update-destroy'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('therapist-profiles/', TherapistProfileListCreateView.as_view(), name='therapistprofile-list-create'),
    path('therapist-profiles/<int:pk>/', TherapistProfileDetailView.as_view(), name='therapistprofile-detail'),
    path('login/', views.MyTokenObtainPairView.as_view()),

]