# Generated by Django 2.1.4 on 2018-12-18 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-created_at',)},
        ),
    ]
