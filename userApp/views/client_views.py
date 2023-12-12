from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from userManagement import settings
import json

keycloak_url = settings.KEYCLOAK_SERVER_URL
realm = settings.KEYCLOAK_REALM
client_id = settings.KEYCLOAK_CLIENT_ID
admin_username = settings.KEYCLOAK_ADMIN_USERNAME
admin_password = settings.KEYCLOAK_ADMIN_PASSWORD

class TokenNotValidException(Exception):
    pass
    

class KeycloakClientView(APIView):

    def get(self,request):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response(response.json())
            return Response({"Error": "Failed to get the clients","response":response.json()}, status=response.status_code)
        
    def post(self,request):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(url, headers=headers,json=request.data)
            if response.status_code == 201:
                return Response({"Message": "Client created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"Error": "Failed to create client","response": response.json()}, status=response.status_code)
        
class KeycloakClientDetailsView(APIView):

    def get(self,request,clientId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response(response.json())
            return Response({"Error": "Failed to obtain client details", "response": response.json()}, status=response.status_code)
    
    def put(self,request,clientId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.put(url, headers=headers,json=request.data)
            if response.status_code == 204:
                return Response({"Message": f"Client '{clientId}' updated successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": f"Failed to update client '{clientId}'","response": response.json()}, status=response.status_code)
    
    def delete(self,request,clientId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return Response({"Message": f"Client '{clientId}' deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": f"Failed to delete client '{clientId}'", "response": response.json()}, status=response.status_code)