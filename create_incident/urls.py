from django.urls import path
from .views import (
    UserCreation,
    UserList, UpdateUser,
    IncidentCreation, IncidentList, UpdateIncident,
    DeleteIncident, SearchIncident, pincodeInformation
)

urlpatterns = [
    path('info/<str:pincode>/', pincodeInformation.as_view(), name='get-pincode-info'),
    path('userregister/', UserCreation.as_view(), name='user-create'),
    path('users/', UserList.as_view(), name='user-list'),
    path('incidents/update/', UpdateIncident.as_view(), name='incident-update'), 
    path('users/update/', UpdateUser.as_view(), name='user-update'),
    path('incidents/list', IncidentList.as_view(), name='incident-list'),
    path('incidents/delete/', DeleteIncident.as_view(), name='incident-delete'),
    path('incidents/search/', SearchIncident.as_view(), name='incident-search'),
    path('incidents/create/', IncidentCreation.as_view(), name='incident-create'),
    
]