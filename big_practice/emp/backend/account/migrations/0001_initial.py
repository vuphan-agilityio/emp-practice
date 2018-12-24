# Generated by Django 2.0 on 2018-12-05 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.SmallIntegerField(default=0, verbose_name='status code activity of user')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='age of user')),
                ('about_me', models.CharField(max_length=400, verbose_name='introduce about me of user')),
                ('birthday', models.DateTimeField(blank=True, null=True, verbose_name='birthday of user')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(blank=True, null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='department.Department', verbose_name='department id')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user id')),
            ],
            options={
                'ordering': ['first_name'],
            },
        ),
    ]
