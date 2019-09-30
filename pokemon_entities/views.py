import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )

    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemons_in_map = PokemonEntity.objects.all()

    for pokemon in pokemons_in_map:

        add_pokemon(folium_map, pokemon.lat, pokemon.lon,
                    pokemon.pokemon.title,
                    request.build_absolute_uri(pokemon.pokemon.image.url))

    pokemons = Pokemon.objects.all()

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request,
                  "mainpage.html",
                  context={
                      'map': folium_map._repr_html_(),
                      'pokemons': pokemons_on_page,
                  })


def show_pokemon(request, pokemon_id):

    try:
        pokemon_name = Pokemon.objects.get(id=int(pokemon_id))
        
    except Pokemon.DoesNotExist as error:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    

    pokemon_entities = PokemonEntity.objects.get(pokemon=pokemon_name)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_info = []

    
    try:
       
        next_evolution=pokemon_entities.evolution_from.get()
      
    except:
        next_evolution = None

    pokemon_info.append({
        'pokemon_id':
        pokemon_entities.pokemon.id,
        'img_url':
        request.build_absolute_uri(pokemon_entities.pokemon.image.url),
        'title_ru':
        pokemon_entities.pokemon.title,
        'title_en':
        pokemon_entities.pokemon.title_en,
        'title_jp':
        pokemon_entities.pokemon.title_jp,
        'description':
        pokemon_entities.pokemon.description,
    })
    if pokemon_entities.evolution:
        pokemon_info[0]['previous_evolution'] = {
            'pokemon_id':
            pokemon_entities.evolution.pokemon.id,
            'title_ru':
            pokemon_entities.evolution.pokemon.title,
            'img_url':
            request.build_absolute_uri(pokemon_entities.evolution.pokemon.image.url)
        }
    if next_evolution:
        pokemon_info[0]['next_evolution'] = {
            'pokemon_id': next_evolution.pokemon.id,
            'title_ru': next_evolution.pokemon.title,
            'img_url': request.build_absolute_uri(next_evolution.pokemon.image.url)
        }

    add_pokemon(folium_map, pokemon_entities.lat, pokemon_entities.lon,
                pokemon_entities.pokemon.title,
                request.build_absolute_uri(pokemon_entities.pokemon.image.url))

    return render(request,
                  "pokemon.html",
                  context={
                      'map': folium_map._repr_html_(),
                      'pokemon': pokemon_info[0]
                  })
