# Generated by Django 5.0.2 on 2024-03-24 06:43

import uuid

import django.utils.timezone
import micro.jango.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Auth",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=255, unique=True, verbose_name="email address")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                (
                    "id",
                    micro.jango.models.fields.ShortIdField(
                        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                        length=11,
                        max_length=20,
                        prefix="A",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("uuid", models.UUIDField(db_index=True, default=uuid.uuid4)),
                ("source", models.CharField(default="slac", max_length=50)),
                ("data", models.JSONField(default=dict, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "auth",
                "verbose_name_plural": "auths",
                "db_table": "auths",
                "ordering": ["email"],
                "abstract": False,
                "swappable": "AUTH_USER_MODEL",
            },
        ),
    ]
