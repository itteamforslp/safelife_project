# Generated by Django 2.1.7 on 2019-03-19 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_auto_20190319_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='studentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student'),
        ),
    ]
