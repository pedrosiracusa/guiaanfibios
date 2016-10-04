# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('speciesguide', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=10)),
                ('abbr_name', models.CharField(max_length=3)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
            ],
        ),
        migrations.AlterField(
            model_name='species',
            name='occurrence_states',
            field=models.ManyToManyField(verbose_name='Estados de Ocorrência', to='speciesguide.State'),
        ),
        migrations.AddField(
            model_name='species',
            name='occurrence_months',
            field=models.ManyToManyField(verbose_name='Meses de Ocorrência', related_name='month_occurring_species', to='speciesguide.Month'),
        ),
    ]
