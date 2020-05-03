# Generated by Django 3.0.5 on 2020-05-01 18:12

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=256, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('secret', models.CharField(max_length=8, unique=True)),
                ('started', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('character_found', models.BooleanField(default=False)),
                ('action_found', models.BooleanField(default=False)),
                ('action', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Action')),
                ('character', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Character')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='backend.Game')),
            ],
            options={
                'unique_together': {('game', 'action'), ('game', 'name'), ('game', 'character')},
            },
        ),
        migrations.AddField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='backend.Player'),
        ),
    ]
