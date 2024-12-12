# Generated by Django 5.1.4 on 2024-12-12 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentimentanalysis',
            name='analysis_result',
        ),
        migrations.AddField(
            model_name='sentimentanalysis',
            name='analysis',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='sentimentanalysis',
            name='name',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='sentimentanalysis',
            name='message',
            field=models.TextField(),
        ),
    ]