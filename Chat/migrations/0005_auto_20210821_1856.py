# Generated by Django 3.2.5 on 2021-08-21 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Chat', '0004_alter_privatechatroom_user1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatechatroom',
            name='user1',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_admin': False}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='roomchatmessage',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
