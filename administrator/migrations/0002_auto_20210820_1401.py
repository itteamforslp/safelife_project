# Generated by Django 3.1.5 on 2021-08-20 21:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterUniqueTogether(
            name='class',
            unique_together={('course', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='courseteacher',
            unique_together={('course', 'teachers')},
        ),
    ]
