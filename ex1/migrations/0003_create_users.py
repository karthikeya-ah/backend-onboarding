from django.db import migrations
from django.contrib.auth.hashers import make_password
import uuid

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
        User.objects.create(
            id=uuid.uuid4(),
            email=u["email"], 
            password=make_password(u["password"])
        )

def clear_users(apps, schema_editor):
    User = apps.get_model("ex1", "CustomUser")
    User.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ("ex1", "0002_seed_data"),              
    ]
   
    operations = [
        migrations.RunPython(create_users, clear_users),
    ]
