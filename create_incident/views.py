from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User as Authorization
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Incident
from .serializers import UserSerializer, IncidentSerializer,GetIncidentSerializer
import requests
import json



class UserCreation(APIView):

    def post(self, request, *args, **kwargs):
    
        pincode = request.data.get('pincode')
        response = requests.get(f'http://127.0.0.1:8000/info/{pincode}/')

        if response.status_code == 200:
            data = response.json()
            request.data['city'] = data.get('city', '')
            request.data['state'] = data.get('state', '')
            request.data['country'] = data.get('country', '')
            
            username = request.data['first_name'] +" "+ request.data['last_name']

            try:
                existing_user = Authorization.objects.get(username=username)
                return Response({'detail': 'Username already there'}, status=status.HTTP_400_BAD_REQUEST)
            except Authorization.DoesNotExist:
                pass  

            User_serializer = UserSerializer(data=request.data)
            User_serializer.is_valid(raise_exception=True)
            hashed_password = make_password(request.data['password'])
            User_serializer.validated_data['password'] = hashed_password
            User_serializer.save()
            
            Authentication = Authorization(
                username=username, 
                email=request.data['email'],
                password=hashed_password,
            )
            Authentication.save()
            return Response({'detail': 'User created successfully'})
        else:
            return Response({'detail': 'error unable to fetch pincode'})


class UserList(APIView):

    def get_queryset(self):
        user_id = self.request.query_params.get('id')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                return [user]
            except User.DoesNotExist:
                raise NotFound("User does not exist")

        return "you are not authorized"

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    


class UpdateUser(APIView):

    def put(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')

        if user_id is None:
            raise ValidationError({'user_id': ['kindly provide the userid']})

        instance = get_object_or_404(User, pk=user_id)

        serializer = UserSerializer(instance, data=request.data)
        

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User updated successfully'})

        return Response(serializer.errors)
    


class pincodeInformation(APIView):

    def get(self, request, *args, **kwargs):
        pincode = self.kwargs['pincode']
        pinendpoint = f'https://api.postalpincode.in/pincode/{pincode}'
        response = requests.get(pinendpoint)

        if response.status_code == 200:
            pincode_information = json.loads(response.text)
            if pincode_information and isinstance(pincode_information, list):
                post_office_info = pincode_information[0].get('PostOffice', [])
                if post_office_info:
                    city = post_office_info[0].get('District', '')
                    state = post_office_info[0].get('State', '')
                    country = post_office_info[0].get('Country', '')
                    return Response({'city': city, 'state': state, 'country': country})

        return Response({'detail': 'Pincode not found'})


class IncidentCreation(APIView):
    serializer_class = IncidentSerializer

    def post(self, request, *args, **kwargs):
        reporter_id = request.data.get('reporters_id')
        print("---------------->", reporter_id)
        
        try:
            reporter = User.objects.get(pk=reporter_id)
            
        except User.DoesNotExist:
            return Response({'detail': 'No Reporter'})

        request.data['reporter_name'] = str(reporter)

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            incident = serializer.save()
            return Response({'detail': 'Incident created successfully'})
        
        return Response(serializer.errors)


class IncidentList(APIView):
    authentication_classes = [BasicAuthentication] 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Incident.objects.filter(reporter_name=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            print("healllo")
            queryset = self.get_queryset()
            serializer = GetIncidentSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UpdateIncident(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        incident_id = self.request.query_params.get('incident_id')
        if incident_id is None:
            raise ValidationError({'incident_id': ['please provide the incident id']})

        try:
            return Incident.objects.get(incident_id=incident_id, reporter_name=self.request.user)
        except Incident.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is None:
            return Response({'detail': 'not authorized'})

        if instance.status == 'Closed':
            return Response({'detail': 'cannot be edited because stause is closed'})

        serializer = IncidentSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Incident updated successfully'})
        
        return Response(serializer.errors)
    

class DeleteIncident(APIView):
    serializer_class = IncidentSerializer

    def get_object(self):
        incident_id = self.request.query_params.get('incident_id')
        if incident_id is None:
            return None

        try:
            return Incident.objects.get(incident_id=incident_id)
        except Incident.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is None:
            return Response({'detail': 'No incident'})

        instance.delete()
        return Response({'detail': 'Incident deleted successfully'})
    



class SearchIncident(APIView):

    def get_queryset(self, incident_id):
        if incident_id:
            return Incident.objects.filter(incident_id=incident_id)
        return Incident.objects.none()

    def get(self, request, *args, **kwargs):
        incident_id = request.query_params.get('incident_id')
        if not incident_id:
            return Response({'detail': 'incident_id not found'})

        try:
            queryset = self.get_queryset(incident_id)
            serializer = GetIncidentSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': 'Error'})