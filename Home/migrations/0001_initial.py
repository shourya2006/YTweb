# Generated by Django 4.0.1 on 2022-01-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('msg_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100000000)),
                ('email', models.CharField(default='', max_length=70000000)),
                ('phone', models.CharField(default='', max_length=7000000)),
                ('msg', models.CharField(default='', max_length=50000000)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_name', models.CharField(max_length=5000000)),
                ('desc', models.TextField(max_length=30000000)),
                ('show_desc', models.CharField(max_length=68, null=True)),
                ('pub_date', models.DateField()),
                ('image', models.ImageField(default='', upload_to='Home/images')),
                ('video', models.URLField(unique=True)),
            ],
        ),
    ]
