# Generated by Django 3.0.8 on 2021-04-11 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PollsRestAPIApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='polloption',
            old_name='vote',
            new_name='Poll',
        ),
    ]