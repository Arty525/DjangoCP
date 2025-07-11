# Generated by Django 5.2.3 on 2025-06-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_alter_customuser_is_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(
                blank=True, upload_to="avatars", verbose_name="Аватар"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="country",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Страна"
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=11, unique=True, verbose_name="Номер телефона"
            ),
        ),
    ]
