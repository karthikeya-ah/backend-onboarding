from django.db import migrations
import random

def assign_users(apps, schema_editor):
    Country = apps.get_model("ex1", "CountryModel")
    User = apps.get_model("ex1", "CustomUser")
    
    users = list(User.objects.all())
    if not users:
        return
    
    for country in Country.objects.all():
        country.my_user = random.choice(users)
        country.save()

class Migration(migrations.Migration):
    dependencies = [
        ('ex1', '0003_create_users'),
    ]

    operations = [
        migrations.RunPython(assign_users),
    ]
