# Generated by Django 4.0.3 on 2022-03-29 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('open_id', models.CharField(max_length=100)),
                ('Type', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=100)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('result', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Query',
            },
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('open_id', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('duration', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'Time',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
