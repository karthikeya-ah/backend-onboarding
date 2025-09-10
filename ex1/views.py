# Turns out django has class based views
# Views are the main business logic of an app
# A route url sends request to a view
# View processes the req, takes in params(if any), queries the db(if needed), returns a response
# Views are responsible for creating, updating, deleting, retrieving, listing data
# DRF view classifies requests into 5 types - list, create, retrieve, update, destroy
# A request (GET, POST, PUT, DELETE) is mapped to one of these types, which is handled within the view class

# Various DRF features used in Views - querysets, serializers, pagination, filtering, permissions, throttling
# querysets - to query the db
# serializers - to convert complex data types (querysets) to native python datatypes (dictionary) that can then be easily rendered into JSON, XML
# pagination - to split large result sets into smaller chunks
# filtering - to filter results based on certain criteria
# permissions - to restrict access to certain views based on user roles
# throttling - to limit the rate of requests to a view
# (see drf docs for more...)

# Viewset - a type of class based view that provides the implementation for all the 5 types of requests
# GenericAPIView - a base class for all class based views


# Authentication - TokenAuthentication, SessionAuthentication, BasicAuthentication
# Permissions - IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
# Throttling - AnonRateThrottle, UserRateThrottle, ScopedRateThrottle
# Filtering - DjangoFilterBackend, SearchFilter, OrderingFilter


# https://www.django-rest-framework.org/api-guide/views/
# https://www.django-rest-framework.org/api-guide/viewsets/


from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.pagination import CursorPagination

from .models import *
from .serializers import *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import authentication

# Auth - Token based signin/signout for CustomUser model
# https://www.django-rest-framework.org/api-guide/authentication/

# POST /signin/  with {username, password} in body
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': str(user.id),
            'email': user.email
        })

# POST /signout/ with 'Authorization: Token <user-token>' in headers
class SignOutView(APIView):
    def post(self, request):
        if request.auth:
            request.auth.delete()
            return Response({'detail': 'Signed out successfully.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Not authenticated.'}, status=status.HTTP_400_BAD_REQUEST)



# GET/POST /countries/
class CountryListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountrySerializer
        
    def get_queryset(self):
        return CountryModel.objects.filter(my_user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(my_user=self.request.user)

# GET/PUT/DELETE /countries/<country_code>/
class CountryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CountrySerializer
    lookup_field = 'country_code'
    
    def get_queryset(self):
        return CountryModel.objects.filter(my_user=self.request.user)

class StateListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StateSerializer
    
    def get_queryset(self):
        country_code = self.kwargs.get('country_code')
        return StateModel.objects.filter(country__country_code=country_code, country__my_user=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        country_code = self.kwargs.get('country_code')
        context['country_code'] = country_code
        return context

class StateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StateSerializer
    lookup_field = 'state_code'
    
    def get_queryset(self):
        country_code = self.kwargs.get('country_code')
        return StateModel.objects.filter(country__country_code=country_code, country__my_user=self.request.user)

class CityListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitySerializer
    
    def get_queryset(self):
        country_code = self.kwargs.get('country_code')
        state_code = self.kwargs.get('state_code')
        return CityModel.objects.filter(
            state__state_code=state_code, 
            state__country__country_code=country_code,
            state__country__my_user=self.request.user
        )

class CityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CitySerializer
    lookup_field = 'city_code'
    
    def get_queryset(self):
        country_code = self.kwargs.get('country_code')
        state_code = self.kwargs.get('state_code')
        return CityModel.objects.filter(
            state__state_code=state_code, 
            state__country__country_code=country_code,
            state__country__my_user=self.request.user
        )


class UserCursorPagination(CursorPagination):
    page_size = 2
    ordering = 'email'

class UserListView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserCursorPagination

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class NestedCountryListCreateView(generics.ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NestedCountrySerializer
    
    def get_queryset(self):
        return CountryModel.objects.all().prefetch_related('states__cities')
    
    def perform_create(self, serializer):
        serializer.save(my_user=self.request.user)


class NestedCountryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NestedCountrySerializer
    lookup_field = 'country_code'
    
    def get_queryset(self):
        return CountryModel.objects.all().prefetch_related('states__cities')