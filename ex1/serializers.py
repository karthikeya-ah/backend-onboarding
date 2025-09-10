# Serializers simplify complex data structures
# Imaging having a model Product (well this is a very complicated model)
# Serializer takes your Product object and converts it into a dictionary, 
# which can then be easily rendered into JSON or XML for Response object

# Django also provides Deserializers
# Takes in user submited data, in json/or xml, converts to Product object model for Django

# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer


from rest_framework import serializers
from .models import *

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryModel
        fields = '__all__'
        read_only_fields = ['id']


class StateSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(source='country.country_code', read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=CountryModel.objects.all(), write_only=True, required=True)
    
    class Meta:
        model = StateModel
        fields = [
            'id',
            'name',
            'gst_code',
            'state_code',
            'country',
            'country_code',
        ]
        read_only_fields = ['id', 'country_code']

    def validate(self, data):
        name = data.get('name')
        country = data.get('country')
        if name and len(name) < 3:
            raise serializers.ValidationError({"name": "State name must be at least 3 characters long"})
        if name and country:
            queryset = StateModel.objects.filter(name=name, country=country)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("State with this name already exists in the country.")
        return data
    
    
class CitySerializer(serializers.ModelSerializer):
    state_code = serializers.CharField(source='state.state_code', read_only=True)
    state = serializers.PrimaryKeyRelatedField(queryset=StateModel.objects.all(), write_only=True, required=True)

    class Meta:
        model = CityModel
        fields = [
            'id',
            'name',
            'city_code',
            'phone_code',
            'population',
            'avg_age',
            'num_of_adults_males',
            'num_of_adults_females',
            'state',
            'state_code',
        ]
        read_only_fields = ['id', 'state_code']

    def validate(self, data):
        name = data.get('name')
        state = data.get('state')
        if name and len(name) < 3:
            raise serializers.ValidationError({"name": "City name must be at least 3 characters long"})
        if name and state:
            queryset = CityModel.objects.filter(name=name, state=state)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("City with this name already exists in the state.")
        return data