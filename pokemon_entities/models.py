from django.db import models


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Название', max_length=200)
    image = models.ImageField(verbose_name='изображение покемона',
                              upload_to='pokemon',
                              null=True,
                              blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    title_en = models.CharField(verbose_name='Название на английском',
                                max_length=20,
                                blank=True)
    title_jp = models.CharField(verbose_name='Название на японском',
                                max_length=20,
                                blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name='entities')
    evolution = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Эволюционирует из',
        related_name='evolution_from'
    )
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появится на карте',db_index=True)
    disappeared_at = models.DateTimeField(verbose_name='Исчезнет с карты',db_index=True)
    level = models.IntegerField(verbose_name='Уровень', default=0)
    health = models.IntegerField(verbose_name='Здоровье', default=100)
    strength = models.IntegerField(verbose_name='Атака', default=0)
    defence = models.IntegerField(verbose_name='Защита', default=0)
    stamina = models.IntegerField(verbose_name='Выносливость', default=0)

    def __str__(self):
        return self.pokemon.title