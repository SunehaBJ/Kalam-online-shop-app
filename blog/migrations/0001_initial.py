# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploader', models.CharField(default='', max_length=200)),
                ('title', models.CharField(default='', max_length=200)),
                ('author', models.CharField(default='', max_length=200)),
                ('genre', models.CharField(choices=[('Fiction', 'Fiction'), ('LoveandRomance', 'LoveandRomance'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('ScienceandFiction', 'ScienceandFiction'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('ActionandAdventure', 'ActionandAdventure'), ('Comedy', 'Comedy'), ('Poetry', 'Poetry'), ('Study', 'Study')], default='fiction', max_length=20)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('image', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='images/')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=200)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('admin', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, default=0.0, null=True)),
                ('no_ratings', models.IntegerField(default=0)),
                ('uploader', models.CharField(default='', max_length=200)),
                ('title', models.CharField(default='', max_length=200)),
                ('author', models.CharField(default='', max_length=200)),
                ('genre', models.CharField(choices=[('Fiction', 'Fiction'), ('LoveandRomance', 'LoveandRomance'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('ScienceandFiction', 'ScienceandFiction'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('ActionandAdventure', 'ActionandAdventure'), ('Comedy', 'Comedy'), ('Poetry', 'Poetry'), ('Study', 'Study')], default='fiction', max_length=20)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('document', models.FileField(upload_to='documents/')),
                ('image', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='images/')),
                ('public', models.BooleanField(default=True)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('searchshow', models.BooleanField(default=True)),
                ('rmembers', models.ManyToManyField(related_name='rmembers', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flist', models.ManyToManyField(related_name='owner1', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_field', multiselectfield.db.fields.MultiSelectField(choices=[('Fiction', 'Fiction'), ('LoveandRomance', 'LoveandRomance'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('ScienceandFiction', 'ScienceandFiction'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('ActionandAdventure', 'ActionandAdventure'), ('Comedy', 'Comedy'), ('Poetry', 'Poetry'), ('Study', 'Study')], max_length=111)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jlist', models.ManyToManyField(related_name='jlist', to='blog.Community')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='images/')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Document')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Readpending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Document')),
                ('rplist', models.ManyToManyField(related_name='rplist', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='community',
            name='documents',
            field=models.ManyToManyField(related_name='docs', to='blog.Document'),
        ),
        migrations.AddField(
            model_name='community',
            name='jrequests',
            field=models.ManyToManyField(related_name='jrequests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]