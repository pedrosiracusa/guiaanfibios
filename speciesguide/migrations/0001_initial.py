# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djgeojson.fields
import speciesguide.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('slug', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('ordering', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Família', max_length=50)),
                ('slug', models.SlugField()),
                ('description', models.TextField(verbose_name='Descrição')),
                ('thematic_hexacolor', models.CharField(verbose_name='Cor Temática', help_text='cor temática da família, em hexadecimal', max_length=7)),
                ('symbol', models.FilePathField()),
            ],
            options={
                'verbose_name_plural': 'Families',
            },
        ),
        migrations.CreateModel(
            name='Habitat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('slug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MediaAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('file', models.FileField(verbose_name='Arquivo', upload_to=speciesguide.models.sp_media_dirpath)),
                ('type', models.CharField(verbose_name='Tipo', choices=[('PICT', 'Fotografia'), ('VIDS', 'Vídeo'), ('SOUN', 'Audio')], default=None, max_length=5)),
                ('datetime', models.DateTimeField(verbose_name='DataHorário')),
                ('copyright', models.CharField(verbose_name='Autoria', max_length=50)),
                ('description', models.TextField(verbose_name='Descrição')),
                ('location', djgeojson.fields.PointField(verbose_name='Localidade', help_text=' ')),
                ('sp_prof_img', models.BooleanField(verbose_name='Foto-perfil', default=False, help_text='Esta é a foto-perfil da espécie')),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Nome científico', max_length=50)),
                ('vernacular', models.CharField(verbose_name='Nome Comum', max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField(verbose_name='Descrição')),
                ('size', models.FloatField(verbose_name='Tamanho', help_text='Insira o tamanho médio em centímetros')),
                ('activity_timing', models.CharField(choices=[('DIUR', 'Diurno'), ('NOCT', 'Noturno')], default=None, max_length=4)),
                ('family', models.ForeignKey(verbose_name='Família', to='speciesguide.Family')),
                ('habitat', models.ManyToManyField(to='speciesguide.Habitat')),
            ],
            options={
                'verbose_name_plural': 'Species',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='species',
            name='occurrence_states',
            field=models.ManyToManyField(verbose_name='Estados de Ocorrência', related_name='occurring_species', to='speciesguide.State'),
        ),
        migrations.AddField(
            model_name='mediaasset',
            name='species',
            field=models.ForeignKey(verbose_name='Espécie', related_name='media', to='speciesguide.Species'),
        ),
        migrations.AddField(
            model_name='article',
            name='species',
            field=models.ManyToManyField(related_name='articles', to='speciesguide.Species'),
        ),
    ]
