# Generated by Django 4.2.4 on 2023-11-29 07:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="user",
        ),
        migrations.DeleteModel(
            name="Customer",
        ),
        migrations.DeleteModel(
            name="UserProfile",
        ),
    ]
