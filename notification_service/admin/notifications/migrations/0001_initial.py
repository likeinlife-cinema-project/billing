# Generated by Django 3.2 on 2023-12-26 09:12

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('slug', models.SlugField(max_length=64, primary_key=True, serialize=False, verbose_name='slug')),
                ('content', models.TextField(verbose_name='content')),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Template',
                'db_table': 'public"."template',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject', models.CharField(max_length=64, verbose_name='subject')),
                ('periodicity', models.DurationField(verbose_name='periodicity')),
                ('start_at', models.DateTimeField(verbose_name='start_at')),
                ('finish_at', models.DateTimeField(verbose_name='finish_at')),
                ('roles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), help_text='User roles. For example: admin, user, subscriber', size=None, verbose_name='roles')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.template', verbose_name='template')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notification',
                'db_table': 'public"."notification',
            },
        ),
    ]