# Generated by Django 5.2.3 on 2025-06-14 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sender", "0004_recipient_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailinglist",
            options={
                "permissions": [
                    ("can_view", "Can view mailing list"),
                    ("can_turn_off", "Can turn off mailing list"),
                ],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="message",
            options={
                "ordering": ["title"],
                "permissions": [("can_view", "Can view message")],
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
            },
        ),
        migrations.AlterModelOptions(
            name="recipient",
            options={
                "ordering": ["email"],
                "permissions": [("can_view", "Can view recipient")],
                "verbose_name": "Получатель",
                "verbose_name_plural": "Получатели",
            },
        ),
        migrations.AddField(
            model_name="mailinglist",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активна"),
        ),
    ]
