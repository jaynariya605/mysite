# Generated by Django 3.2.5 on 2021-08-26 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0007_auto_20210817_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvals',
            name='Feedback',
            field=models.CharField(blank=True, choices=[('0', 'Approved'), ('1', 'Rejected')], max_length=115),
        ),
    ]
