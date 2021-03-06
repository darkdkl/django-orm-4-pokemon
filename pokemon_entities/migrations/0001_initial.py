# Generated by Django 2.2.6 on 2019-11-10 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pokemon', verbose_name='изображение покемона')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('title_en', models.CharField(blank=True, max_length=20, verbose_name='Название на английском')),
                ('title_jp', models.CharField(blank=True, max_length=20, verbose_name='Название на японском')),
                ('evolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evolution_from', to='pokemon_entities.Pokemon', verbose_name='Эволюционирует из')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('lon', models.FloatField(verbose_name='Долгота')),
                ('appeared_at', models.DateTimeField(db_index=True, verbose_name='Появится на карте')),
                ('disappeared_at', models.DateTimeField(db_index=True, verbose_name='Исчезнет с карты')),
                ('level', models.IntegerField(default=0, verbose_name='Уровень')),
                ('health', models.IntegerField(default=100, verbose_name='Здоровье')),
                ('strength', models.IntegerField(default=0, verbose_name='Атака')),
                ('defence', models.IntegerField(default=0, verbose_name='Защита')),
                ('stamina', models.IntegerField(default=0, verbose_name='Выносливость')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity', to='pokemon_entities.Pokemon')),
            ],
        ),
    ]
