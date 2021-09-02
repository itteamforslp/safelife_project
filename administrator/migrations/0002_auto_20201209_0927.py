# Generated by Django 3.1.1 on 2020-12-09 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='classes',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='students',
        ),
        migrations.AddField(
            model_name='attendance',
            name='class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_identitfication', to='administrator.class'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attendance',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.student'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_of_attendance', to='administrator.class'),
        ),
    ]