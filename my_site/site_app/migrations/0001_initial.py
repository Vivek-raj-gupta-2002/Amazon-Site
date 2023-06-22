# Generated by Django 4.2.2 on 2023-06-19 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Catogery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_link', models.URLField()),
                ('collection', models.BooleanField(default=1)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_app.catogery')),
            ],
        ),
        migrations.CreateModel(
            name='Collected_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000)),
                ('rating', models.CharField(blank=True, max_length=1000)),
                ('review', models.CharField(blank=True, max_length=1000)),
                ('isAvaliable', models.CharField(blank=True, max_length=1000)),
                ('price', models.CharField(blank=True, max_length=1000)),
                ('mrp', models.CharField(blank=True, max_length=1000)),
                ('seller', models.CharField(blank=True, max_length=1000)),
                ('ASIN', models.CharField(blank=True, max_length=1000)),
                ('First_date', models.CharField(blank=True, max_length=1000)),
                ('created', models.DateTimeField(auto_now=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_app.link')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AddConstraint(
            model_name='catogery',
            constraint=models.UniqueConstraint(fields=('user', 'name'), name='unique_per_user_field'),
        ),
    ]
