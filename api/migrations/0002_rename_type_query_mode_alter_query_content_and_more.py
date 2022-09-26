# Generated by Django 4.0.3 on 2022-03-29 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='Type',
            new_name='mode',
        ),
        migrations.AlterField(
            model_name='query',
            name='content',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='query',
            name='result',
            field=models.CharField(max_length=1024),
        ),
    ]