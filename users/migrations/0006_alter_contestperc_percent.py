# Generated by Django 5.1 on 2024-11-07 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_contestperc_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestperc',
            name='percent',
            field=models.FloatField(),
        ),
    ]
