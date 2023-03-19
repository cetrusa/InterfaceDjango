# Generated by Django 4.1.5 on 2023-03-12 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_database_users_delete_permissiondb'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='users',
        ),
        migrations.AddField(
            model_name='user',
            name='databases',
            field=models.ManyToManyField(blank=True, to='users.database'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('databases', models.ManyToManyField(to='users.database')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
