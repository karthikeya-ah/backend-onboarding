from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_users(apps, schema_editor):
    User = apps.get_model("ex1", "CustomUser")

    users = [
        {"email": "a@ah.com", "password": "test123"},
        {"email": "b@ah.com", "password": "test123"},
        {"email": "c@ah.com", "password": "test123"},
        {"email": "d@ah.com", "password": "test123"},
        {"email": "e@ah.com", "password": "test123"},
    ]

    for u in users:
        User.objects.create(email=u["email"], password=make_password(u["password"]))

class Migration(migrations.Migration):
    dependencies = [
        ("ex1", "0002_seed_data"),              
    ]
   
    operations = [
        migrations.RunPython(create_users),
    ]
