# Generated by Django 4.2 on 2024-08-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_category_name_category_unique_name_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthaccesstoken',
            name='meta',
            field=models.TextField(default=None, max_length=500, null=True),
        ),
    ]
