# Generated by Django 4.2.1 on 2023-05-23 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0006_delete_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviews',
            options={'ordering': ['-created_at']},
        ),
    ]
