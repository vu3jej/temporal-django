# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-09 02:26
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion
import temporal_django.db_extensions
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vclock', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=100)),
                ('number', models.IntegerField()),
                ('effective_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemClock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('tick', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example_app.ItemActivity')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clock', related_query_name='clocks', to='example_app.Item')),
            ],
            options={
                'db_table': 'example_app_item_clock',
                'ordering': ['tick'],
            },
        ),
        migrations.CreateModel(
            name='ItemHistory_effective_date',
            fields=[
                ('effective_date', models.DateField()),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('effective', django.contrib.postgres.fields.ranges.DateTimeRangeField()),
                ('vclock', django.contrib.postgres.fields.ranges.IntegerRangeField()),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='effective_date_history', to='example_app.Item')),
            ],
            options={
                'db_table': 'example_app_item_history_effective_date',
            },
        ),
        migrations.CreateModel(
            name='ItemHistory_number',
            fields=[
                ('number', models.IntegerField()),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('effective', django.contrib.postgres.fields.ranges.DateTimeRangeField()),
                ('vclock', django.contrib.postgres.fields.ranges.IntegerRangeField()),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='number_history', to='example_app.Item')),
            ],
            options={
                'db_table': 'example_app_item_history_number',
            },
        ),
        migrations.CreateModel(
            name='ItemHistory_title',
            fields=[
                ('title', models.CharField(max_length=100)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('effective', django.contrib.postgres.fields.ranges.DateTimeRangeField()),
                ('vclock', django.contrib.postgres.fields.ranges.IntegerRangeField()),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_history', to='example_app.Item')),
            ],
            options={
                'db_table': 'example_app_item_history_title',
            },
        ),
        migrations.AddIndex(
            model_name='itemhistory_title',
            index=temporal_django.db_extensions.GistExclusionConstraint(fields=['(entity_id) WITH =, effective WITH &&'], name='example_app_item_history_title_excl_effective'),
        ),
        migrations.AddIndex(
            model_name='itemhistory_title',
            index=temporal_django.db_extensions.GistExclusionConstraint(fields=['(entity_id) WITH =, vclock WITH &&'], name='example_app_item_history_title_excl_vclock'),
        ),
        migrations.AddIndex(
            model_name='itemhistory_number',
            index=temporal_django.db_extensions.GistExclusionConstraint(fields=['(entity_id) WITH =, effective WITH &&'], name='example_app_item_history_number_excl_effective'),
        ),
        migrations.AddIndex(
            model_name='itemhistory_number',
            index=temporal_django.db_extensions.GistExclusionConstraint(fields=['(entity_id) WITH =, vclock WITH &&'], name='example_app_item_history_number_excl_vclock'),
        ),
        migrations.AddIndex(
            model_name='itemhistory_effective_date',
            index=temporal_django.db_extensions.GistExclusionConstraint(fields=['(entity_id) WITH =, effective WITH &&'], name='example_app_item_history_effective_date_excl_effective'),
        ),
        migrations.AddIndex(
            model_name='itemhistory_effective_date',
            index=temporal_django.db_extensions.GistExclusionConstraint(fields=['(entity_id) WITH =, vclock WITH &&'], name='example_app_item_history_effective_date_excl_vclock'),
        ),
        migrations.AlterUniqueTogether(
            name='itemclock',
            unique_together=set([('entity', 'activity'), ('tick', 'entity')]),
        ),
    ]
