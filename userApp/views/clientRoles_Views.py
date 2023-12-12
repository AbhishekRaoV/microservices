from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from rest_framework.request import Request

keycloak_url = settings.KEYCLOAK_SERVER_URL
realm=settings.KEYCLOAK_REALM
clientId = settings.KEYCLOAK_CLIENT_ID

class clientRolesView(APIView):

    def get(self, request, client_id):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        getRoles_url = f'{keycloak_url}/admin/realms/{realm}/clients/{client_id}/roles'        
        headers = {
                    'Authorization': f'Bearer {access_token}',
                    }
        
        try:
            response = requests.get(getRoles_url,headers=headers)
            # print(response.json())
            if response.status_code == 200:
                return Response(response.json())
            elif response.status_code == 401:
                return Response({"message":"Not authorized"}, status = response.status_code)
            else:
                return Response({'error': 'Failed to fetch roles'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)
        
class userClientRolesView(APIView):
    #print("hello user")
    def get(self, request, user_id, client_id):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        getuserRoles_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/role-mappings/clients/{client_id}'
        #print(getuserRoles_url)
             
        headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                    }
        
        try:
            response = requests.get(getuserRoles_url,headers=headers)
            #print(response.json())
            if response.status_code == 200:
                return Response(response.json())
            elif response.status_code == 401:
                return Response({"message":"Not authorized"}, status = response.status_code)
            else:
                return Response({'error': 'Failed to fetch roles for the user'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)

    def post(self, request, user_id, client_id):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        getuserRoles_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/role-mappings/clients/{client_id}'     
        headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                    }
        print(request.data)
        try:
            response = requests.post(getuserRoles_url, json=request.data, headers=headers)
            # print(response.json())
            if response.status_code == 204:
                return Response({"message":"User added to the role successfully"}, status = response.status_code)
            elif response.status_code == 401:
                return Response({"message":"Not authorized"}, status = response.status_code)
            else:
                return Response({'error': 'Failed to add roles for the user'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)

