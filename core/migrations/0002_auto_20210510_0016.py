# Generated by Django 3.1 on 2021-05-09 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('officeId', models.CharField(max_length=100)),
                ('image', models.CharField(max_length=200)),
                ('face', models.CharField(max_length=200)),
                ('UserId', models.IntegerField()),
                ('GroupId', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Calls',
        ),
    ]
