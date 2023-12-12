from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from rest_framework.request import Request

keycloak_url = settings.KEYCLOAK_SERVER_URL
realm=settings.KEYCLOAK_REALM
clientId = settings.KEYCLOAK_CLIENT_ID

class realmRolesView(APIView):

    def get(self, request):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        getRoles_url = f'{keycloak_url}/admin/realms/{realm}/roles'
        
        headers = {
                    'Authorization': f'Bearer {access_token}',
            }
        
        try:
            response = requests.get(getRoles_url,headers=headers)
            print(response)
            if response.status_code == 200:
                return Response(response.json())
            elif response.status_code == 401:
                return Response({"message":"Not authorized"}, status = response.status_code)
            else:
                return Response({'error': 'Failed to fetch roles'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)
        
    def post(self, request):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]

        getRoles_url = f'{keycloak_url}/admin/realms/{realm}/roles'
        
        headers = {
                    'Authorization': f'Bearer {access_token}',
                    "Content-Type": "application/json"
            }
        
        try:
            response = requests.post(getRoles_url,json=request.data,headers=headers)
            print(response)
            if response.status_code == 201:
                return Response({"message":"Realm role created successfully"}, status = response.status_code)
            elif response.status_code == 409:
                return Response({"message":"user already exist with same username or email_id,"}, status = response.status_code)
            elif response.status_code == 401:
                return Response({"message":"Not authorized"}, status = response.status_code)
            else:
                return Response({'error': 'Failed to create roles'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)


class RealmRoleDetailView(APIView):

    def get(self, request,roleName, *args, **kwargs):
        #get a perticular user details
        #Retrieve the Keycloak access token
        auth_header = request.headers.get("Authorization", None)
        print(auth_header)
        access_token = auth_header.split(' ')[1]
        if access_token:
            getRoles_url = f'{keycloak_url}/admin/realms/{realm}/roles/{roleName}'
            
            #get_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/role-mappings/clients/{client}/available'
            headers = {
                'Authorization': f'Bearer {access_token}' 
                }
            
            try:
                response = requests.get(getRoles_url,headers=headers)
                print(response)
                if response.status_code == 200:
                    return Response(response.json())
                elif response.status_code == 401:
                    return Response({"message":"Not authorized"}, status = response.status_code)
                else:
                    return Response({'error': 'Failed to fetch role details'}, status=response.status_code)
            except requests.exceptions.RequestException as e:
                return Response({'error': f'Error: {str(e)}'}, status=500)
            
                 
    def put(self, request, roleName):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            getRoles_url = f'{keycloak_url}/admin/realms/{realm}/roles/{roleName}'
            
            #get_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/role-mappings/clients/{client}/available'
            headers = {
                'Authorization': f'Bearer {access_token}' 
                'Content-Type": "application/json'
                }
            
            try:
                response = requests.put(getRoles_url,headers=headers,json=request.data)
                print(response)
                if response.status_code == 204:
                    return Response({"message":"Role updated successfully"}, status = response.status_code)
                elif response.status_code == 409:
                    return Response({"message":"user already exist with same username or email_id,"}, status = response.status_code)
                elif response.status_code == 401:
                    return Response({"message":"Not authorized"}, status = response.status_code)
                else:
                    return Response({'error': 'Failed to fetch role details'}, status=response.status_code)
            except requests.exceptions.RequestException as e:
                return Response({'error': f'Error: {str(e)}'}, status=500)
            
             
    def delete(self, request, roleName):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            getRoles_url = f'{keycloak_url}/admin/realms/{realm}/roles/{roleName}'
            
            #get_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/role-mappings/clients/{client}/available'
            headers = {
                'Authorization': f'Bearer {access_token}' 
                'Content-Type": "application/json'
                }
            
            try:
                response = requests.delete(getRoles_url,headers=headers)
                print(response)
                if response.status_code == 204:
                    return Response({"message":"Role deleted successfully"}, status = response.status_code)
                elif response.status_code == 401:
                    return Response({"message":"Not authorized"}, status = response.status_code)
                else:
                    return Response({'error': 'Failed to fetch role details'}, status=response.status_code)
            except requests.exceptions.RequestException as e:
                return Response({'error': f'Error: {str(e)}'}, status=500)
            
             
    