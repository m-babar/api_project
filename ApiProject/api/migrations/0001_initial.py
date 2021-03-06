# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-15 07:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=52, verbose_name='Title')),
                ('Uid', models.UUIDField(blank=True, editable=False)),
                ('Uri', models.URLField(max_length=512, verbose_name='URI')),
                ('Type', models.CharField(choices=[('MOVIE', 'MOVIE'), ('TVSHOW', 'TVSHOW'), ('ADVERTISEMENT', 'ADVERTISEMENT'), ('BUMPER', 'BUMPER'), ('PROMO', 'PROMO')], default='TVSHOW', max_length=10, verbose_name='Type')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_assest', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=52, verbose_name='Title')),
                ('Uid', models.UUIDField(blank=True, editable=False)),
                ('Status', models.CharField(choices=[('PROCESSING', 'PROCESSING'), ('ENCODING ', 'ENCODING '), ('COMPLETED', 'COMPLETED'), ('SCHEDULED', 'SCHEDULED'), ('PLAYING', 'PLAYING')], default='PROCESSING', max_length=10, verbose_name='Status')),
                ('CreatedOn', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('CompletedOn', models.DateTimeField(auto_now_add=True, verbose_name='Completed on')),
                ('Uri', models.URLField(max_length=512, verbose_name='URL')),
                ('ProcessedOn', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('ScheduledOn', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('Duration', models.TimeField(auto_now_add=True, verbose_name='Duration')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_playlist', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=52, verbose_name='Title')),
                ('Uid', models.UUIDField(blank=True, editable=False)),
                ('StartAt', models.DateTimeField(verbose_name='StartAt')),
                ('isLoop', models.BooleanField(verbose_name='is loop')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_schedule', to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='api.Playlist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='assest',
            name='playlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assests', to='api.Playlist'),
        ),
    ]
