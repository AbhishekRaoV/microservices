from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
from userManagement import settings
import json

keycloak_url = settings.KEYCLOAK_SERVER_URL
realm = settings.KEYCLOAK_REALM

class TokenNotValidException(Exception):
    pass
    
class KeycloakGroupView(APIView):

    def get(self,request):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            groups_url = f'{keycloak_url}/admin/realms/{realm}/groups'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(groups_url, headers=headers)
            if response.status_code == 200:
                return Response(response.json())
            return Response({"Error": "Failed to get the groups","response":response.json()}, status=response.status_code)
    
    def post(self,request):       
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/groups'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(url, headers=headers,json=request.data)
            if response.status_code == 201:
                return Response({"Message": "Group created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"Error": "Failed to create group","response": response.json()}, status=response.status_code)

class KeycloakGroupDetailView(APIView):

    def get(self,request,groupId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/groups/{groupId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response(response.json())
            return Response({"Error": "Failed to obtain group details", "response": response.json()}, status=response.status_code)

    def put(self,request,groupId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/groups/{groupId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.put(url, headers=headers,json=request.data)
            if response.status_code == 204:
                return Response({"Message": f"Group '{groupId}' updated successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": f"Failed to update group '{groupId}'","response": response.json()}, status=response.status_code)

    def delete(self,request,groupId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/groups/{groupId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return Response({"Message": f"Group '{groupId}' deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": f"Failed to delete group '{groupId}'", "response": response.json()}, status=response.status_code)


class KeycloakUserGroupsView(APIView):

    def get(self,request,userId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/users/{userId}/groups'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response(response.json())
            return Response({"Error": "Failed to obtain user group details", "response": response.json()}, status=response.status_code)


class KeycloakUserGroupActionsView(APIView):

    def put(self,request,userId,groupId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/users/{userId}/groups/{groupId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.put(url, headers=headers)
            if response.status_code == 204:
                return Response({"Message": f"User '{userId}' added to Group '{groupId}' successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": "Failed to Add user to group","response": response.json()}, status=response.status_code)
       

    def delete(self,request,userId,groupId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/users/{userId}/groups/{groupId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                return Response({"Message": f"User '{userId}' left the Group '{groupId}' successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": "Failed to left from group","response": response.json()}, status=response.status_code)
