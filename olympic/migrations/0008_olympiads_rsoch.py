# Generated by Django 4.2.1 on 2023-06-07 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('olympic', '0007_secrettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='olympiads',
            name='rsoch',
            field=models.BooleanField(default=0, max_length=2000, verbose_name='Входит ли в перечень?'),
            preserve_default=False,
        ),
    ]
