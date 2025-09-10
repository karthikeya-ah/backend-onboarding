from django.urls import path
from .views import (
    CustomObtainAuthToken, SignOutView, UserListView, UserCreateView, UserRetrieveUpdateDestroyView,
    CountryListCreateView, CountryRetrieveUpdateDestroyView,
    StateListCreateView, StateRetrieveUpdateDestroyView,
    CityListCreateView, CityRetrieveUpdateDestroyView,
    NestedCountryListCreateView, NestedCountryRetrieveUpdateDestroyView
)
from django.urls import path

app_name = 'ex1'

urlpatterns = [
    # auth
    path('auth/signin/', CustomObtainAuthToken.as_view(), name='auth-signin'),
    path('auth/signout/', SignOutView.as_view(), name='auth-signout'),
    
    # user
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<uuid:id>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),

    # nested country-state-city
    path('nested/countries/', NestedCountryListCreateView.as_view(), name='nested-country-list-create'),
    path('nested/countries/<str:country_code>/', NestedCountryRetrieveUpdateDestroyView.as_view(), name='nested-country-retrieve-update-destroy'),

    # Individual entity endpoints
    path('countries/', CountryListCreateView.as_view(), name='country-list-create'),
    path('countries/<str:country_code>/', CountryRetrieveUpdateDestroyView.as_view(), name='country-retrieve-update-destroy'),

    # state
    path('countries/<str:country_code>/states/', StateListCreateView.as_view(), name='state-list-create'),
    path('countries/<str:country_code>/states/<str:state_code>/', StateRetrieveUpdateDestroyView.as_view(), name='state-retrieve-update-destroy'),

    # city
    path('countries/<str:country_code>/states/<str:state_code>/cities/', CityListCreateView.as_view(), name='city-list-create'),
    path('countries/<str:country_code>/states/<str:state_code>/cities/<str:city_code>/', CityRetrieveUpdateDestroyView.as_view(), name='city-retrieve-update-destroy'),
]
