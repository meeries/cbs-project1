from django.db import migrations

def create_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.create_user('username', 'user@example.com', 'password')

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user),
    ]
