# Generated by Django 4.2.1 on 2023-06-06 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olympic', '0006_alter_notificationdates_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecretToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(max_length=2000, verbose_name='Telegram id')),
                ('secret_token', models.CharField(max_length=2000, verbose_name='Секретный Токен')),
            ],
            options={
                'verbose_name': 'Секретный Токен',
                'verbose_name_plural': 'Секретные Токены',
                'ordering': ['telegram_id'],
            },
        ),
    ]
