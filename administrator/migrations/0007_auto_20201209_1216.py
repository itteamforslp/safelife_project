# Generated by Django 3.1.1 on 2020-12-09 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_auto_20201209_1113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='classid',
        ),
        migrations.AlterField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.course'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
