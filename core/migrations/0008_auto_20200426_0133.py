# Generated by Django 3.0.5 on 2020-04-26 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200426_0108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='quantitiy',
            new_name='quantity',
        ),
    ]
