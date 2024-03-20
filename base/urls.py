from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PatientListCreateView, PatientRetrieveUpdateDestroyView, AppointmentDetailView,AppointmentListCreateView,ProfileRetrieveUpdateDestroyView, UserRegistrationView,  PatientAppointmentListView,ProfileListCreateView,SendResetPassword, change_password_view,EditProfileView,CancelPatientStatusView

from . import views
from .views import UserRegistrationView
urlpatterns = [
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateDestroyView.as_view(), name='patient-retrieve-update-destroy'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.MyTokenObtainPairView.as_view()),
    path('patients/<int:pk>/appointments/', PatientAppointmentListView.as_view(), name='patient-appointments'),
    path('profiles/<int:user_id>/', ProfileRetrieveUpdateDestroyView.as_view(), name='profile-detail'),
    path('profiles/create/<int:user_id>/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('sendResetEmail/', SendResetPassword.as_view(), name='send_reset_email'),
    path('reset-password/<int:user_id>/', change_password_view, name='change-password'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('patients/<int:pk>/cancel/', CancelPatientStatusView.as_view(), name='cancel-patient-status'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
