# Generated by Django 3.1.1 on 2020-12-10 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_auto_20201209_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_identifier', to='administrator.course'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.class'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.student'),
        ),
    ]
