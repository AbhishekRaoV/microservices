import requests
from cryptography.fernet import Fernet
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from django.conf import settings
from rest_framework.views import APIView
import jwt
from datetime import datetime

encryption_key = b'ki5VJhbSKADEsVG_Veou2pxddZFe2MFG3aJdsUp-PFA='
access_token = None
def decrypt_password(encrypted_password):
    try:
        cipher_suite = Fernet(encryption_key)
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    except Exception as e:
        return None
    
def generate_token(request):
        # print(type(request))
        # print("the request is: ", request.data)
        plaintext_username = request.data['username']
        encrypted_password = request.data['password']
        decrypted_password = decrypt_password(encrypted_password)
        payload = {
            'client_id': settings.KEYCLOAK_CLIENT_ID,
            'grant_type': 'password',
            'username': plaintext_username,
            'password': decrypted_password
        }
        headers =  {"content-type": "application/x-www-form-urlencoded"}
        token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
        response = requests.post(token_url, data=payload, headers=headers)
        #print("response is:", response)
        return response
        
            
class userLoginView(APIView):
    def post_queryset(self,request):
        access_token=generate_token(request)
        if access_token:
            return access_token.json()
        else:
            return Response({'message': 'Token generation failed'}, status=401)

    def post(self,request, *args, **kwargs):
        queryset = self.post_queryset(request)
        #serializer=KeycloakUserSerializer(queryset,many=True)
        #print("Access Token from global: ",login_encrypt_views.access_token)
        access_token = queryset.get('access_token')
        token = {'data': {'access_token':access_token } }
        try:
            decoded_token = jwt.decode(access_token, options={"verify_signature": False})
            #print(decoded_token)
            #token keys =['exp','iat', 'jti', 'iss', 'sub', 'typ', 'azp', 'session_state','acr', 'scope', 'sid', 'email_verified', 'name', 'preferred_username', 'given_name', 'family_name', 'email']
            if 'exp' in decoded_token:
                current_time = datetime.utcnow().timestamp()
                if decoded_token['exp'] < current_time:
                    return Response({"message": "Token has expired"}, status = 401)
            return Response(token)

        except jwt.DecodeError:
            return JsonResponse({"message": "Invalid credentials, please provide the valid username and password"}, status = 401)
        except jwt.InvalidTokenError:
            return Response({"message": "Invalid Token"}, status = 401)
    
    
