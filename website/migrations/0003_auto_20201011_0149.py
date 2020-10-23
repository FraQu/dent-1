# Generated by Django 3.1.1 on 2020-10-10 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20201010_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speciality', models.CharField(blank=True, max_length=255, null=True)),
                ('updated_date', models.DateField(auto_now_add=True, null=True)),
                ('email', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
            managers=[
                ('objects', website.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.doctor'),
        ),
    ]