# Generated by Django 5.1.6 on 2025-03-20 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pfp',
            name='image',
            field=models.ImageField(default='default/user_default.png', upload_to='profile_pics/'),
        ),
    ]
