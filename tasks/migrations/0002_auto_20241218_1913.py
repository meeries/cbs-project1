from django.db import migrations

def create_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.create_user('Alligator', 'user@example.com', 'Crocodile')

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user),
    ]
