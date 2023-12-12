# appname/views.py

from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from rest_framework.request import Request
import json

keycloak_url = settings.KEYCLOAK_SERVER_URL
realm=settings.KEYCLOAK_REALM   
client_id = settings.KEYCLOAK_CLIENTID                      

class KeycloakUserListView(APIView):

    def get_queryset(self, request):
        #get the users list api    
        #Retrieve the Keycloak access token from header
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
    
        if access_token:            
            users_url = f'{keycloak_url}/admin/realms/{realm}/users'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(users_url, headers=headers)
            if response.status_code == 200:
                return response.json()
        else:
            return Response({'message': 'Access token not found in headers'}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self,request):
        queryset = self.get_queryset(request)
        return Response(queryset)                

    def add_role(self, request, user_id, headers):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        getuserRoles_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/role-mappings/clients/{client_id}'     
    
        role_id = request.data.get('role_id')
        role_name = request.data.get('role_name')
        data=[
                {
                    "id": role_id,
                    "name": role_name
                }
            ]
        try:
            response = requests.post(getuserRoles_url, json=data, headers=headers)
            # print(response.json())
            if response.status_code == 204:
                return Response({"message":f"User added to the {role_name} successfully"}, status = response.status_code)
            elif response.status_code == 401:
                return Response({"message":"Not authorized"}, status = response.status_code)
            else:
                return Response({'error': 'Failed to add roles for the user'}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)
    
    def add_group(self, request, user_id, headers):
         
        group_ids = request.data.get('groups')
        if group_ids:
            for group_id in group_ids:
                add_to_group_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/groups/{group_id}'
            
                try:
                    response = requests.put(add_to_group_url, headers=headers)
                    # print(response.json())
                    if response.status_code == 204:
                        return Response({"message":"User added to the Group successfully"}, status = response.status_code)
                    elif response.status_code == 401:
                        return Response({"message":"Not authorized"}, status = response.status_code)
                    else:
                        return Response({'error': 'Failed to add user to the groups'}, status=response.status_code)
                except requests.exceptions.RequestException as e:
                    return Response({'error': f'Error: {str(e)}'}, status=500)
        else:
            pass
        
    def post(self,request,*args,**kwargs):
        #Create user API        
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=400)

        # Create the user data payload
        user_data = {
            'username': username,
            'enabled': True,  # You can customize user attributes here
            'credentials': [{'type': 'password', 'value': password}],
        }
        users_url = f'{keycloak_url}/admin/realms/{realm}/users'
        headers = {
                    'Authorization': f'Bearer {access_token}',
                    "Content-Type": "application/json"
            }
        
        try:
            response = requests.post(users_url, data=json.dumps(user_data), headers=headers)
            # print("user created response", response.headers)
            if response.status_code == 201:
                # print('user respone is ',response)
                location_header = response.headers.get("Location")
                if location_header:
                    user_id = location_header.split("/")[-1]
                    addRole = self.add_role(request, user_id, headers)
                    addGroup = self.add_group(request, user_id, headers)
                    print(addRole)
                    print(addGroup)
                else:
                    return Response("User ID not found in Location header", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'message': 'User created successfully'})
            elif response.status_code == 409:
                return Response({"message":"user already exist with same username or email_id"}, status = response.status_code)
            elif response.status_code == 401:
                return Response({"message":"Not authorized"}, status = response.status_code)
            else:
                return Response({'error': 'Failed to create user'}, status=response.status_code)
                            
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)
        

class KeycloakUserDetailView(APIView):
    
    def get(self, request,user_id, *args, **kwargs):
        #get a perticular user details
        #Retrieve the Keycloak access token
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            get_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}'
            headers = {
                 'Authorization': f'Bearer {access_token}' ,
                  }
            response = requests.get(get_url, headers=headers)
            print("get response:",response)
            if response.status_code ==200:
                return Response(response.json(), status = status.HTTP_200_OK)
            elif response.status_code ==401:
                return Response({"message":"Not Authorized"}, status = response.status_code)
            else:
                return Response({"message":"User not found"}, status = response.status_code)

    def put(self, request,user_id, *args, **kwargs):
        #Update the user detalis
        #Retrieve the Keycloak access token
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            put_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}'
            headers = {'Authorization': f'Bearer {access_token}',
                        'Content-Type':'application/json',                                                                                                                                    }
            response = requests.put(put_url,json=request.data, headers=headers)
            print("put response:",response)
            if response.status_code ==204:
                return Response({"message":"User updated successfully"}, status = status.HTTP_200_OK)
            elif response.status_code ==401:
                return Response({"message":"Not Authorized"}, status = response.status_code)
            elif response.status_code == 409:
                return Response({"message":"user already exists with same email id "}, status = response.status_code)
            else:
                return Response({"message":"User update failed"}, status = response.status_code)

    def delete(self, request,user_id, *args, **kwargs):
        #Delete a user
        #Retrieve the Keycloak access token
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            delete_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}'
            headers = {'Authorization': f'Bearer {access_token}',}
            response = requests.delete(delete_url, headers=headers)
            print("Delete response:",response)
            if response.status_code ==204:
                return Response({"message":"User Deleted successfully"}, status = status.HTTP_204_NO_CONTENT)
            elif response.status_code ==401:
                return Response({"message":"Not Authorized"}, status = response.status_code)
            else: 
                return Response({"message":"User deletion failed"}, status = response.status_code)
