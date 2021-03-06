# Generated by Django 3.2.5 on 2021-08-26 20:02

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django_countries.fields
import listings.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=64)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('place_type', models.CharField(choices=[('ONLINE', 'online'), ('IRL', 'in person')], default='IRL', max_length=16)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicelisting_set', to='main.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicelisting_set', to='users.seller')),
                ('tags', models.ManyToManyField(blank=True, related_name='servicelisting_set', to='main.Tag')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='ItemListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=64)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('weight', models.FloatField(validators=[listings.validators.weight_validator])),
                ('made_in', django_countries.fields.CountryField(max_length=2)),
                ('color', models.CharField(choices=[('WHITE', 'white'), ('BLACK', 'black'), ('GREY', 'grey'), ('RED', 'red'), ('GREEN', 'green'), ('BLUE', 'blue'), ('YELLOW', 'yellow'), ('PURPLE', 'purple'), ('ORANGE', 'orange'), ('PINK', 'pink')], default='WHITE', max_length=16)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itemlisting_set', to='main.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='itemlisting_set', to='users.seller')),
                ('tags', models.ManyToManyField(blank=True, related_name='itemlisting_set', to='main.Tag')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='AutoListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=64)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('weight', models.FloatField(validators=[listings.validators.weight_validator])),
                ('made_in', django_countries.fields.CountryField(max_length=2)),
                ('color', models.CharField(choices=[('WHITE', 'white'), ('BLACK', 'black'), ('GREY', 'grey'), ('RED', 'red'), ('GREEN', 'green'), ('BLUE', 'blue'), ('YELLOW', 'yellow'), ('PURPLE', 'purple'), ('ORANGE', 'orange'), ('PINK', 'pink')], default='WHITE', max_length=16)),
                ('condition', models.CharField(choices=[('NEW', 'new'), ('USED', 'used')], default='NEW', max_length=8)),
                ('mileage', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='autolisting_set', to='main.category')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='autolisting_set', to='users.seller')),
                ('tags', models.ManyToManyField(blank=True, related_name='autolisting_set', to='main.Tag')),
            ],
            options={
                'verbose_name': 'auto',
                'verbose_name_plural': 'autos',
            },
        ),
        migrations.CreateModel(
            name='AutoProxy',
            fields=[
            ],
            options={
                'ordering': ['date_created'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('listings.autolisting',),
            managers=[
                ('lastweek_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ItemProxy',
            fields=[
            ],
            options={
                'ordering': ['date_created'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('listings.itemlisting',),
            managers=[
                ('lastweek_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ServiceProxy',
            fields=[
            ],
            options={
                'ordering': ['date_created'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('listings.servicelisting',),
            managers=[
                ('lastweek_objects', django.db.models.manager.Manager()),
            ],
        ),
    ]
