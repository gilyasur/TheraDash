from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import PatientListCreateView, PatientRetrieveUpdateDestroyView, AppointmentDetailView,AppointmentListCreateView,ProfileRetrieveUpdateDestroyView, UserRegistrationView,  PatientAppointmentListView,ProfileListCreateView

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


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
