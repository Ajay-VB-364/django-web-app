# Generated by Django 4.1.5 on 2023-02-02 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_recipe_ingredients_remove_recipe_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_support',
            field=models.BooleanField(default=False),
        ),
    ]
