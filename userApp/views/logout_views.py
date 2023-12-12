import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

keycloak_url = settings.KEYCLOAK_SERVER_URL
realm=settings.KEYCLOAK_REALM   
client_id = settings.KEYCLOAK_CLIENTID 

class LogoutView(APIView):

    def post(self, request, user_id):
        # Define the URL for the Keycloak logout endpoint
        logout_url = f'{keycloak_url}/admin/realms/{realm}/users/{user_id}/logout'
        auth_header = request.headers.get("Authorization", None)
        access_token = auth_header.split(' ')[1]
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = requests.post(logout_url, headers=headers)

            if response.status_code == 204:
                # A successful logout request should return a 204 No Content status
                return Response("Logout successful", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(f"Failed to log out. Status code: {response.status_code}", status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error: {str(e)}'}, status=500)