# Generated by Django 3.1 on 2020-11-06 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20201105_1107'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('created',)},
        ),
        migrations.RemoveField(
            model_name='product',
            name='other_image',
        ),
        migrations.AddField(
            model_name='product',
            name='second_image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='product',
            name='third_image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
