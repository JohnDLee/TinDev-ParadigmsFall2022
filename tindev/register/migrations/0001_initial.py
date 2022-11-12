# Generated by Django 3.2.13 on 2022-11-11 02:09

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateProfile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('zip_code', models.IntegerField(validators=[django.core.validators.MinLengthValidator(5, 'Zip Code must be 5 digits.'), django.core.validators.MaxLengthValidator(5, 'Zip Code must be 5 digits.')], verbose_name='Zip Code')),
                ('bio', models.CharField(max_length=500, verbose_name='Profile Bio')),
                ('skills', models.TextField(verbose_name='Skills')),
                ('github', models.CharField(max_length=200, verbose_name='Github Username')),
                ('experience', models.PositiveSmallIntegerField(verbose_name='Years Of Experience')),
                ('education', models.TextField(verbose_name='Education')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='RecruiterProfile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('zip_code', models.IntegerField(validators=[django.core.validators.MinLengthValidator(5, 'Zip Code must be 5 digits.'), django.core.validators.MaxLengthValidator(5, 'Zip Code must be 5 digits.')], verbose_name='Zip Code')),
                ('company', models.CharField(max_length=200, verbose_name='Company')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
