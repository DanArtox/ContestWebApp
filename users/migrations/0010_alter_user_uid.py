# Generated by Django 5.1 on 2024-12-02 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_checkingdatas_ltype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
