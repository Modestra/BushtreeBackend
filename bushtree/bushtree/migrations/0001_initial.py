# Generated by Django 4.1.13 on 2024-08-29 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flowers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('frozen_resistance', models.CharField(max_length=5)),
                ('sunlight', models.CharField(max_length=20)),
                ('period_blossom_start', models.TextField()),
                ('period_blossom_end', models.TextField()),
                ('height', models.PositiveBigIntegerField(default=0)),
                ('color_bloss_name', models.CharField(max_length=20)),
                ('color_bloss_hex', models.CharField(max_length=8)),
                ('color_leaves_name', models.CharField(max_length=20)),
                ('color_leaves_hex', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Seccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('date', models.TextField()),
            ],
        ),
    ]
