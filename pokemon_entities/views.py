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

    pokemons_in_map=PokemonEntity.objects.all()

    

    for pokemon in pokemons_in_map:
       
        add_pokemon(folium_map, pokemon.lat, pokemon.lon,
                pokemon.pokemon.title, request.build_absolute_uri(pokemon.pokemon.image.url))

    pokemons=Pokemon.objects.all()
    
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
   

    try:
        pokemon_name=Pokemon.objects.get(id=int(pokemon_id))
    except:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entity=PokemonEntity.objects.filter(pokemon=pokemon_name)
    
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_info = []
  

    for pokemon in pokemon_entity:
        try:
            next_evolution=Pokemon.objects.get(entity__evolution=pokemon)
        except:
            next_evolution=None
        
        pokemon_info.append({
            'pokemon_id': pokemon.pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.pokemon.image.url),
            'title_ru': pokemon.pokemon.title,
            'title_en': pokemon.pokemon.title_en ,
            'title_jp': pokemon.pokemon.title_jp,
            'description':pokemon.pokemon.description,
             })
        if pokemon.evolution:
            pokemon_info[0]['previous_evolution']={'pokemon_id': pokemon.evolution.pokemon.id,'title_ru': pokemon.evolution.pokemon.title,
            'img_url': request.build_absolute_uri(pokemon.evolution.pokemon.image.url) }
        if next_evolution:
            pokemon_info[0]['next_evolution']={'pokemon_id':next_evolution.id,'title_ru': next_evolution.title,'img_url': request.build_absolute_uri(next_evolution.image.url)}
        


        add_pokemon(folium_map, pokemon.lat, pokemon.lon, pokemon.pokemon.title, request.build_absolute_uri(pokemon.pokemon.image.url))

        

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_info[0] })


