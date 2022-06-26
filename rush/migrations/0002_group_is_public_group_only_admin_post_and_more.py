# Generated by Django 4.0.4 on 2022-06-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rush', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='is_public',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='group',
            name='only_admin_post',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='group',
            name='banner',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='picture',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='GroupConfig',
        ),
    ]