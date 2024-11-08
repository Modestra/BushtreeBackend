# Generated by Django 4.1 on 2024-09-20 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bushtree', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='garden',
            name='name',
        ),
        migrations.AddField(
            model_name='garden',
            name='url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='garden',
            name='image',
            field=models.ImageField(upload_to='media/'),
        ),
    ]