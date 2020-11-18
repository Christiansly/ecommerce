# Generated by Django 3.1 on 2020-11-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20201102_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ManyToManyField(blank=True, null=True, to='shop.Image'),
        ),
        migrations.RemoveField(
            model_name='product',
            name='variation',
        ),
        migrations.AddField(
            model_name='product',
            name='variation',
            field=models.ManyToManyField(blank=True, null=True, to='shop.Variation'),
        ),
    ]