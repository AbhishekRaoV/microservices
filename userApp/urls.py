"""
URL configuration for userManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from userApp.views import views
from rest_framework.routers import DefaultRouter

from userApp.views import group_views, login_encrypt_views, userRoles_views, views, logout_views
from .views.views import KeycloakUserListView
from .views.views import KeycloakUserDetailView
from .views.group_views import KeycloakGroupView,KeycloakGroupDetailView,KeycloakUserGroupsView,KeycloakUserGroupActionsView
from .views.client_views import KeycloakClientView,KeycloakClientDetailsView
from .views.resource_views import KeycloakResourceView,KeycloakResourceDetailView
from django.contrib import admin
from .views.login_encrypt_views import userLoginView
from .views.userRoles_views import realmRolesView, RealmRoleDetailView
from .views.clientRoles_Views import clientRolesView, userClientRolesView
from .views.logout_views import LogoutView

#from .views import KeycloakUserUpdateView
# router = DefaultRouter()
# router.register(r'users', KeycloakUserListCreate, basename='user')

urlpatterns = [
   # ... other URL patterns
   # path('api/', include(router.urls)),
    path('login/', login_encrypt_views.userLoginView.as_view()),
    path('users/',views.KeycloakUserListView.as_view()),
    path('groups/', KeycloakGroupView.as_view()),
    path('groups/<str:groupId>/', KeycloakGroupDetailView.as_view()),
    path('userGroups/<str:userId>/', KeycloakUserGroupsView.as_view()),
    path('userGroups/<str:userId>/<str:groupId>/', KeycloakUserGroupActionsView.as_view()),
    path('clients/', KeycloakClientView.as_view()),
    path('clients/<str:clientId>/', KeycloakClientDetailsView.as_view()),
    path('resources/<str:clientId>/', KeycloakResourceView.as_view()),
    path('resources/<str:clientId>/<str:resourceId>/', KeycloakResourceDetailView.as_view()),
    path('users/<str:user_id>/', KeycloakUserDetailView.as_view(), name = 'keycloak-user-detail'),
    path('roles/<str:client_id>/', clientRolesView.as_view(), name = 'client roles'),
    path('roles/<str:user_id>/<str:client_id>/', userClientRolesView.as_view(), name = 'user client roles'),
    path('logout/<str:user_id>/', LogoutView.as_view(), name='logout'), 
]

# urlpatterns += router.urls
