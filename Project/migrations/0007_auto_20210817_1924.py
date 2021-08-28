# Generated by Django 3.2.5 on 2021-08-17 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Project', '0006_auto_20210817_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvals',
            name='Result',
            field=models.CharField(choices=[('0', 'Approved'), ('1', 'Rejected')], default=0, max_length=115),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='approvals',
            name='date_modified',
            field=models.DateField(auto_now=True, verbose_name='last modified'),
        ),
        migrations.AlterField(
            model_name='approvals',
            name='date_published',
            field=models.DateField(auto_now_add=True, verbose_name='date joined'),
        ),
    ]
