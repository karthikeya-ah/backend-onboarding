from .models import CountryModel, StateModel, CityModel

# input -> http request
# output -> json (serialized data)

# Insert data to state, city and country tables
def insert_country(request):
    country = request.data
    CountryModel.objects.create(    
        name=country['name'],
        country_code=country['country_code'],
        curr_symbol=country['curr_symbol'],
        phone_code=country['phone_code']
    )
    return True
    
def insert_state(request):
    state = request.data
    StateModel.objects.create(
        name=state['name'],
        gst_code=state.get('gst_code', None),
        state_code=state['state_code'],
        country=CountryModel.objects.get(country_code=state['country_code'])
    )
    
    return True
    
def insert_city(request):
    city = request.data
    CityModel.objects.create(
        name=city['name'],
        state=StateModel.objects.get(state_code=city['state_code'])
    )
    
    return True
    
# Bulk insert countries
def bulk_insert_countries(request):
    countries = request.data
    country_objects = [
        CountryModel(
            name=country['name'],
            country_code=country['country_code'],
            curr_symbol=country['curr_symbol'],
            phone_code=country['phone_code']
        ) for country in countries
    ]
    
    CountryModel.objects.bulk_create(country_objects)

    return True

# Bulk update countries
def bulk_update_countries(request):
    countries = request.data
    country_objects = []
    
    for country in countries:
        try:
            country_obj = CountryModel.objects.get(country_code=country['country_code'])
            country_obj.name = country.get('name', country_obj.name)
            country_obj.curr_symbol = country.get('curr_symbol', country_obj.curr_symbol)
            country_obj.phone_code = country.get('phone_code', country_obj.phone_code)
            country_objects.append(country_obj)
        except CountryModel.DoesNotExist:
            continue
    
    CountryModel.objects.bulk_update(country_objects, ['name', 'curr_symbol', 'phone_code'])
    
    return True
    
def get_all_countries():
    return CountryModel.objects.all()


def get_states_by_country(country_code):
    return StateModel.objects.filter(country__country_code=country_code)

def get_cities_by_state(country_code, state_code):
    return CityModel.objects.filter(state__state_code=state_code, state__country__country_code=country_code)

