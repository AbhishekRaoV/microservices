from django.shortcuts import render
from userApp.serializers import UserSerializer
from userApp.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

#GET all users and Create user(Non Primary key operations)
class UserList(APIView):
    def get(self,request):
        users=User.objects.all()
        serializer=UserSerializer(users,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#GET user by id, Edit and Delete user (Primary Key operations)
class UserDetails(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Http404
    
    def get(self,request,pk):
        user=self.get_object(pk)
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    def put(self,request,pk):
        user=self.get_object(pk)
        serializer = UserSerializer(user,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        user=self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)