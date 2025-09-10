# Turns out django has class based views
# Views are the main business logic of an app
# A route url sends request to a view
# View processes the req, takes in params(if any), queries the db(if needed), returns a response
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

# https://www.django-rest-framework.org/api-guide/views/
# https://www.django-rest-framework.org/api-guide/viewsets/


from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .models import *
from .serializers import *


class CountryViewSet(viewsets.ViewSet):
    lookup_field = 'country_code'
    
    # GET /countries/
    def list(self, request):
        queryset = CountryModel.objects.all()
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # GET /countries/{country_code}/
    def retrieve(self, request, country_code=None):
        queryset = CountryModel.objects.all()
        country = generics.get_object_or_404(queryset, country_code=country_code)
        serializer = CountrySerializer(country)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # POST /countries/
    def create(self, request):
        serializer = CountrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # POST /countries/bulk_insert/
    @action(detail=False, methods=['post'])
    def bulk_insert(self, request):
        serializer = CountrySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT /countries/bulk_update/
    @action(detail=False, methods=['put'])
    def bulk_update(self, request):
        countries_data = request.data
        errors = []
        for country_data in countries_data:
            country_code = country_data.get('country_code')
            try:
                country = CountryModel.objects.get(country_code=country_code)
                serializer = CountrySerializer(country, data=country_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append({country_code: serializer.errors})
            except CountryModel.DoesNotExist:
                errors.append({country_code: 'Not found'})
        return Response({'errors': errors}, status=status.HTTP_200_OK)



class StateViewSet(viewsets.ViewSet):
    lookup_field = 'state_code'
    
        
    # GET country/{country_code}/states/
    def list(self, request, country_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        queryset = StateModel.objects.filter(country=country)
        serializer = StateSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # GET country/{country_code}/states/{state_code}/
    def retrieve(self, request, country_code=None, state_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        queryset = StateModel.objects.filter(country=country)
        state = generics.get_object_or_404(queryset, state_code=state_code)
        serializer = StateSerializer(state)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # POST country/{country_code}/states/
    def create(self, request, country_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        data = request.data
        data['country'] = str(country.id)
        serializer = StateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # POST country/{country_code}/states/bulk_insert/
    @action(detail=False, methods=['post'])
    def bulk_insert(self, request, country_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        states_data = request.data
        for state_data in states_data:
            state_data['country'] = str(country.id)
        serializer = StateSerializer(data=states_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # PUT country/{country_code}/states/bulk_update
    @action(detail=False, methods=['put'])
    def bulk_update(self, request, country_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        new_states_data = request.data
        errors = []
        for state_data in new_states_data:
            state_code = state_data.get('state_code')
            try:
                state = StateModel.objects.get(state_code=state_code, country=country)
                serializer = StateSerializer(state, data=state_data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append({state_code: serializer.errors})
            except StateModel.DoesNotExist:
                errors.append({state_code: 'Not found'})
        return Response({'errors': errors}, status=status.HTTP_200_OK)
        
        
class CityViewSet(viewsets.ViewSet):
    lookup_field = 'city_code'
    
    # GET country/{country_code}/states/{state_code}/cities/
    def list(self, request, country_code=None, state_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        state = generics.get_object_or_404(StateModel, state_code=state_code, country=country)
        queryset = CityModel.objects.filter(state=state)
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # GET country/{country_code}/states/{state_code}/cities/{city_code}/
    def retrieve(self, request, country_code=None, state_code=None, city_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        state = generics.get_object_or_404(StateModel, state_code=state_code, country=country)
        queryset = CityModel.objects.filter(state=state)
        city = generics.get_object_or_404(queryset, city_code=city_code)
        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # POST country/{country_code}/states/{state_code}/cities/
    def create(self, request, country_code=None, state_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        state = generics.get_object_or_404(StateModel, state_code=state_code, country=country)
        data = request.data
        data['state'] = str(state.id)
        serializer = CitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # GET country/{country_code}/cities
    @action(detail=False, methods=['get'])
    def list_cities_in_country(self, request, country_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        states = StateModel.objects.filter(country=country)
        queryset = CityModel.objects.filter(state__in=states)
        serializer = CitySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    # GET country/{country_code}/cities/?min_population=&max_population=
    @action(detail=False, methods=['get'])
    def list_cities_in_country_with_population_filter(self, request, country_code=None):
        country = generics.get_object_or_404(CountryModel, country_code=country_code)
        states = StateModel.objects.filter(country=country)

        min_p = request.query_params.get('min_population', None)
        max_p = request.query_params.get('max_population', None)
        
        queryset = CityModel.objects.filter(states__in=states)
        
        if min_p is not None:
            queryset = queryset.filter(population__gte=min_p)
        if max_p is not None:
            queryset = queryset.filter(population__lte=max_p)
            
        serializer = CitySerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        