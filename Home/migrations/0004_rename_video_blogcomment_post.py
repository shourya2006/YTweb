# Generated by Django 4.0.1 on 2022-01-27 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_blogcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogcomment',
            old_name='video',
            new_name='post',
        ),
    ]
