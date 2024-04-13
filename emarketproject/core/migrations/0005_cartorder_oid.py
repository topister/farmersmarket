# Generated by Django 5.0.3 on 2024-04-12 10:43

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_cartorder_coupons"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartorder",
            name="oid",
            field=shortuuid.django_fields.ShortUUIDField(
                alphabet="0123456789",
                blank=True,
                length=5,
                max_length=10,
                null=True,
                prefix="",
            ),
        ),
    ]