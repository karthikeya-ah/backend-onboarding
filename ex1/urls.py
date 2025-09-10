from django.urls import path, include
from .views import CountryViewSet, StateViewSet, CityViewSet
from django.urls import path

app_name = 'ex1'

country_list = CountryViewSet.as_view({
	'get': 'list',
	'post': 'create',
})
country_detail = CountryViewSet.as_view({
	'get': 'retrieve',
})
country_bulk_insert = CountryViewSet.as_view({
	'post': 'bulk_insert',
})
country_bulk_update = CountryViewSet.as_view({
	'put': 'bulk_update',
})

state_list = StateViewSet.as_view({
	'get': 'list',
	'post': 'create',
})
state_detail = StateViewSet.as_view({
	'get': 'retrieve',
})
state_bulk_insert = StateViewSet.as_view({
	'post': 'bulk_insert',
})
state_bulk_update = StateViewSet.as_view({
	'put': 'bulk_update',
})

city_list = CityViewSet.as_view({
	'get': 'list',
	'post': 'create',
})
city_detail = CityViewSet.as_view({
	'get': 'retrieve',
})

city_list_in_country = CityViewSet.as_view({
	'get': 'list_cities_in_country',
})
city_list_in_country_with_population_filter = CityViewSet.as_view({
	'get': 'list_cities_in_country_with_population_filter',
})

urlpatterns = [
	path('countries/', country_list, name='country-list'),
	path('countries/<str:country_code>/', country_detail, name='country-detail'),
	path('countries/bulk_insert', country_bulk_insert, name='country-bulk-insert'),
	path('countries/bulk_update/', country_bulk_update, name='country-bulk-update'),

	path('countries/<str:country_code>/states/', state_list, name='state-list'),
	path('countries/<str:country_code>/states/bulk_insert/', state_bulk_insert, name='state-bulk-insert'),
	path('countries/<str:country_code>/states/bulk_update/', state_bulk_update, name='state-bulk-update'),
	path('countries/<str:country_code>/states/<str:state_code>/', state_detail, name='state-detail'),

	path('countries/<str:country_code>/states/<str:state_code>/cities/', city_list, name='city-list'),
	path('countries/<str:country_code>/states/<str:state_code>/cities/<str:city_code>/', city_detail, name='city-detail'),

	path('countries/<str:country_code>/cities/', city_list_in_country, name='city-list-in-country'),
	path('countries/<str:country_code>/cities/filter/', city_list_in_country_with_population_filter, name='city-list-in-country-with-population-filter'),
]
