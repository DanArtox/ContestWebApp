# Generated by Django 5.1 on 2024-11-07 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_contestperc_delete_percentage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestPerc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.TextField()),
                ('percent', models.IntegerField()),
                ('cid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Percentage',
            fields=[
                ('name', models.TextField(primary_key=True, serialize=False)),
                ('percent', models.IntegerField()),
            ],
        ),
    ]
