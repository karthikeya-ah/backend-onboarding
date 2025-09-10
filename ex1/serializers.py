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
        fields = ['id', 'name', 'country_code', 'curr_symbol', 'phone_code', 'my_user']
        read_only_fields = ['id', 'my_user']
        
    def validate_phone_code(self, value):
        queryset = CountryModel.objects.filter(phone_code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Phone code already exists.")
        return value


class StateSerializer(serializers.ModelSerializer):
    country_code = serializers.CharField(source='country.country_code', read_only=True)
    my_country__name = serializers.SerializerMethodField(read_only=True)
    my_country__my_user__name = serializers.SerializerMethodField(read_only=True)
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
            'my_country__name',
            'my_country__my_user__name',
        ]
        read_only_fields = ['id', 'country_code', 'my_country__name', 'my_country__my_user__name']

    def get_my_country__name(self, obj):
        return obj.country.name if obj.country else None
        
    def get_my_country__my_user__name(self, obj):
        return obj.country.my_user.email if obj.country and obj.country.my_user else None

    def validate_gst_code(self, value):
        if value:
            queryset = StateModel.objects.filter(gst_code=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("GST code already exists.")
        return value

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
    my_state__name = serializers.SerializerMethodField(read_only=True)
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
            'my_state__name',
        ]
        read_only_fields = ['id', 'state_code', 'my_state__name']

    def get_my_state__name(self, obj):
        return obj.state.name if obj.state else None

    def validate_phone_code(self, value):
        queryset = CityModel.objects.filter(phone_code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Phone code already exists.")
        return value

    def validate_city_code(self, value):
        queryset = CityModel.objects.filter(city_code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("City code already exists.")
        return value

    def validate(self, data):
        name = data.get('name')
        state = data.get('state')
        population = data.get('population')
        num_of_adults_males = data.get('num_of_adults_males')
        num_of_adults_females = data.get('num_of_adults_females')
        
        if name and len(name) < 3:
            raise serializers.ValidationError({"name": "City name must be at least 3 characters long"})
        
        if name and state:
            queryset = CityModel.objects.filter(name=name, state=state)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("City with this name already exists in the state.")
        
        if population is not None and num_of_adults_males is not None and num_of_adults_females is not None:
            if population <= (num_of_adults_males + num_of_adults_females):
                raise serializers.ValidationError("Population must be greater than the sum of adult males and females.")
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class NestedCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = [
            'id', 'name', 'city_code', 'phone_code', 'population',
            'avg_age', 'num_of_adults_males', 'num_of_adults_females'
        ]
        read_only_fields = ['id']

    def validate_phone_code(self, value):
        queryset = CityModel.objects.filter(phone_code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Phone code already exists.")
        return value

    def validate_city_code(self, value):
        queryset = CityModel.objects.filter(city_code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("City code already exists.")
        return value

    def validate(self, data):
        population = data.get('population')
        num_of_adults_males = data.get('num_of_adults_males')
        num_of_adults_females = data.get('num_of_adults_females')
        
        if population is not None and num_of_adults_males is not None and num_of_adults_females is not None:
            if population <= (num_of_adults_males + num_of_adults_females):
                raise serializers.ValidationError("Population must be greater than the sum of adult males and females.")
        
        return data


class NestedStateSerializer(serializers.ModelSerializer):
    cities = NestedCitySerializer(many=True, required=False)
    
    class Meta:
        model = StateModel
        fields = ['id', 'name', 'gst_code', 'state_code', 'cities']
        read_only_fields = ['id']

    def validate_gst_code(self, value):
        if value:
            queryset = StateModel.objects.filter(gst_code=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError("GST code already exists.")
        return value


class NestedCountrySerializer(serializers.ModelSerializer):
    states = NestedStateSerializer(many=True, required=False)
    
    class Meta:
        model = CountryModel
        fields = ['id', 'name', 'country_code', 'curr_symbol', 'phone_code', 'states']
        read_only_fields = ['id']
        
    def validate_phone_code(self, value):
        queryset = CountryModel.objects.filter(phone_code=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Phone code already exists.")
        return value

    def create(self, validated_data):
        states_data = validated_data.pop('states', [])
        country = CountryModel.objects.create(**validated_data)
        
        for state_data in states_data:
            cities_data = state_data.pop('cities', [])
            state = StateModel.objects.create(country=country, **state_data)
            
            for city_data in cities_data:
                CityModel.objects.create(state=state, **city_data)
                
        return country

    def update(self, instance, validated_data):
        states_data = validated_data.pop('states', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if states_data:
            # here its cities will be deleted too because of cascade delete in model
            instance.states.all().delete()
            
            for state_data in states_data:
                cities_data = state_data.pop('cities', [])
                state = StateModel.objects.create(country=instance, **state_data)
                
                for city_data in cities_data:
                    CityModel.objects.create(state=state, **city_data)
        
        return instance