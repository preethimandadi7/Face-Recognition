# Generated by Django 3.1 on 2021-05-11 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210511_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='face',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='member',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]