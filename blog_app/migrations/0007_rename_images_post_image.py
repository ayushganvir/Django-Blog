# Generated by Django 4.0.3 on 2022-05-30 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0006_remove_comment_email_remove_comment_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='images',
            new_name='image',
        ),
    ]
