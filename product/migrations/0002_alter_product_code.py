# Generated by Django 4.2.5 on 2023-09-18 21:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="code",
            field=models.CharField(default=uuid.uuid4, max_length=255, unique=True),
        ),
    ]