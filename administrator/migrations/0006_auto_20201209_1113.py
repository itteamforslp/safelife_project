# Generated by Django 3.1.1 on 2020-12-09 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_auto_20201209_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=''),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.BooleanField(default='FALSE'),
        ),
    ]
