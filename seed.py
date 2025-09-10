import uuid
from ex1.models import CountryModel, StateModel, CityModel  # change ex1 to your app name

def run():
    print("Clearing old data...")
    CityModel.objects.all().delete()
    StateModel.objects.all().delete()
    CountryModel.objects.all().delete()

    print("Inserting new data...")

    # --- Countries ---
    c1 = CountryModel.objects.create(
        id=uuid.uuid4(),
        name="United States",
        country_code="US",
        curr_symbol="$",
        phone_code="+1"
    )

    c2 = CountryModel.objects.create(
        id=uuid.uuid4(),
        name="India",
        country_code="IN",
        curr_symbol="₹",
        phone_code="+91"
    )

    # --- States ---
    s1 = StateModel.objects.create(id=uuid.uuid4(), name="California", gst_code=None, state_code="CA", country=c1)
    s2 = StateModel.objects.create(id=uuid.uuid4(), name="Texas", gst_code=None, state_code="TX", country=c1)
    s3 = StateModel.objects.create(id=uuid.uuid4(), name="New York", gst_code=None, state_code="NY", country=c1)
    s4 = StateModel.objects.create(id=uuid.uuid4(), name="Maharashtra", gst_code="27", state_code="MH", country=c2)
    s5 = StateModel.objects.create(id=uuid.uuid4(), name="Karnataka", gst_code="29", state_code="KA", country=c2)

    # --- Cities ---
    CityModel.objects.create(id=uuid.uuid4(), name="Los Angeles", city_code="LA", phone_code="+1-213",
        population=4000000, avg_age=35.5, num_of_adults_males=2000000, num_of_adults_females=2000000, state=s1)
    CityModel.objects.create(id=uuid.uuid4(), name="San Francisco", city_code="SF", phone_code="+1-415",
        population=870000, avg_age=36.2, num_of_adults_males=430000, num_of_adults_females=440000, state=s1)

    CityModel.objects.create(id=uuid.uuid4(), name="Houston", city_code="HOU", phone_code="+1-713",
        population=2300000, avg_age=34.8, num_of_adults_males=1150000, num_of_adults_females=1150000, state=s2)
    CityModel.objects.create(id=uuid.uuid4(), name="Dallas", city_code="DAL", phone_code="+1-214",
        population=1300000, avg_age=33.5, num_of_adults_males=650000, num_of_adults_females=650000, state=s2)

    CityModel.objects.create(id=uuid.uuid4(), name="New York City", city_code="NYC", phone_code="+1-212",
        population=8400000, avg_age=37.2, num_of_adults_males=4200000, num_of_adults_females=4200000, state=s3)
    CityModel.objects.create(id=uuid.uuid4(), name="Buffalo", city_code="BUF", phone_code="+1-716",
        population=255000, avg_age=38.0, num_of_adults_males=125000, num_of_adults_females=130000, state=s3)

    CityModel.objects.create(id=uuid.uuid4(), name="Mumbai", city_code="MUM", phone_code="+91-22",
        population=12400000, avg_age=29.4, num_of_adults_males=6200000, num_of_adults_females=6200000, state=s4)
    CityModel.objects.create(id=uuid.uuid4(), name="Pune", city_code="PUN", phone_code="+91-20",
        population=3100000, avg_age=28.7, num_of_adults_males=1550000, num_of_adults_females=1550000, state=s4)

    CityModel.objects.create(id=uuid.uuid4(), name="Bangalore", city_code="BLR", phone_code="+91-80",
        population=8400000, avg_age=30.8, num_of_adults_males=4200000, num_of_adults_females=4200000, state=s5)
    CityModel.objects.create(id=uuid.uuid4(), name="Mysore", city_code="MYS", phone_code="+91-821",
        population=920000, avg_age=31.2, num_of_adults_males=460000, num_of_adults_females=460000, state=s5)

    print("✅ Database seeded successfully!")