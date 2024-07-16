# Generated by Django 5.0.7 on 2024-07-16 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordle', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guess',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='guess',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='guess',
            name='guess_info',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='guess',
            name='is_correct',
            field=models.BooleanField(),
        ),
    ]
