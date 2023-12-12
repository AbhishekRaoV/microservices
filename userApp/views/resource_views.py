from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
from userManagement import settings

keycloak_url = settings.KEYCLOAK_SERVER_URL
realm = settings.KEYCLOAK_REALM

class TokenNotValidException(Exception):
    pass
    
class KeycloakResourceView(APIView):

    def get(self,request,clientId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/resource'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return Response(response.json())
            return Response({"Error": "Failed to get the resources of client","response":response.json()}, status=response.status_code)
    
    def post(self,request,clientId):       
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        print(request.data)
        resource_name = request.data["name"]
        resource_uri = request.data["uri"]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/resource'
            headers = {'Authorization': f'Bearer {access_token}'}
            body = {"name": resource_name, "uri": resource_uri}
            response = requests.post(url, headers=headers,json=body)
            if response.status_code == 201:
                if "user" in request.data.keys():
                    # Creating user policy 
                    user = request.data["user"]
                    user_policy_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/policy/user'
                    user_policy_name = f'{resource_name}-UserPolicy'
                    body = {"type":"user","logic":"POSITIVE","decisionStrategy":"UNANIMOUS","name": user_policy_name,"users": [user],"description":"User policy for accessing the resource"}
                    response = requests.post(user_policy_url, headers=headers,json=body)
                    if response.status_code == 201:
                        print("User Policy created successfully")
                        final_policy = user_policy_name
                    else:
                        print("Failed to create Policy")
                        return Response({"Error": "Failed to create user policy for resource","response": response.json()}, status=response.status_code)
                if "group" in request.data.keys():
                    group = request.data["group"]
                    group_policy_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/policy/group'
                    group_policy_name = f'{resource_name}-GroupPolicy'
                    body = {"type":"group","logic":"POSITIVE","decisionStrategy":"UNANIMOUS","name":group_policy_name,"groups":[{"id":group,"path":f'/{group}'}]}
                    response = requests.post(group_policy_url,headers=headers,json=body)
                    final_policy = group_policy_name
                    if not response.status_code==201:
                        return Response({"Error": "Failed to create group policy for resource","response": response.json()}, status=response.status_code)
                # Creating Resource Permissions
                resource_permission_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/permission/resource'
                resource_permission_name = f'{resource_name}-Permission'
                body = {"type":"resource","logic":"POSITIVE","decisionStrategy":"UNANIMOUS","name": resource_permission_name,"resources":[resource_name],"policies":[final_policy]}
                response = requests.post(resource_permission_url, headers=headers,json=body)
                if response.status_code == 201:
                    print("User permission created")
                else: 
                    print("Failed to Create permissions for users")
                    return Response({"Error": "Failed to create user permissions","response": response.json()}, status=response.status_code)
                return Response({"Message": "Resource created successfully"}, status=status.HTTP_201_CREATED)
            return Response({"Error": "Failed to create resource","response": response.json()}, status=response.status_code)
        
    def delete(self,request,clientId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        #import pdb; pdb.set_trace()
        resource_name = request.data["name"]
        if access_token:
            #Get the resource with resource name
            resource_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/resource/search?name={resource_name}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(resource_url, headers=headers)
            if response:
                # Delete the resource
                resource_id = response.json()["_id"]
                resource_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/resource/{resource_id}'
                response = requests.delete(resource_url,headers=headers)
                if response.status_code == 204:
                    # Get the policy associated with resource
                    policy_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/policy/search?name={resource_name}-UserPolicy'
                    response = requests.get(policy_url, headers=headers)
                    if not response.status_code == 200:
                        policy_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/policy/search?name={resource_name}-GroupPolicy'
                        response = requests.get(policy_url, headers=headers)
                        # Delete the associated policy
                    policy_id = response.json()["id"]
                    policy_url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/policy/{policy_id}'
                    response = requests.delete(policy_url, headers=headers)
                    if response.status_code == 204:
                        print("Policy Deleted Successfully")
                    else:
                        return Response({"Error": f"Failed to delete policy '{resource_name}-UserPolicy'", "response": response}, status=response.status_code)
                return Response({"Message": f"Resource '{resource_name}' deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": f"Failed to delete resource '{resource_name}'", "response": response.json()}, status=response.status_code)

class KeycloakResourceDetailView(APIView):

    def put(self,request,clientId,resourceId):
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        if access_token:
            url = f'{keycloak_url}/admin/realms/{realm}/clients/{clientId}/authz/resource-server/resource/{resourceId}'
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.put(url, headers=headers,json=request.data)
            if response.status_code == 204:
                return Response({"Message": f"Resource '{resourceId}' updated successfully"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"Error": f"Failed to update resource '{resourceId}'","response": response.json()}, status=response.status_code)

    