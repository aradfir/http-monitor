# Generated by Django 4.1.5 on 2023-01-26 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="URL",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.URLField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("error_threshold", models.IntegerField(default=10)),
                ("error_count", models.IntegerField(default=0)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="urls",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HeartBeat",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "url",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="heartbeats",
                        to="monitoring.url",
                    ),
                ),
            ],
        ),
    ]
