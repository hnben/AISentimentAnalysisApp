# Generated by Django 5.1.4 on 2024-12-12 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SentimentAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(unique=True)),
                ('analysis_result', models.JSONField()),
            ],
        ),
    ]
