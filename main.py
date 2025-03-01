from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_pokemon_data(name: str):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
    if response.status_code == 200:
        pokemon = response.json()
        
        # Get species data for more info
        species_response = requests.get(pokemon['species']['url'])
        species_data = species_response.json()
        
        # Get type weaknesses/strengths
        type_data = []
        for t in pokemon['types']:
            type_response = requests.get(t['type']['url'])
            type_data.append(type_response.json())
        
        return {
            "pokemon": pokemon,
            "species": species_data,
            "type_info": type_data
        }
    return None

def process_type_relations(type_data):
    damage_relations = {
        'double_damage_from': set(),
        'double_damage_to': set(),
        'half_damage_from': set(),
        'half_damage_to': set(),
        'no_damage_from': set(),
        'no_damage_to': set()
    }
    
    for t in type_data:
        for relation in damage_relations.keys():
            damage_relations[relation].update(
                [x['name'] for x in t['damage_relations'][relation]]
            )
    
    # Calculate net weaknesses/strengths
    weaknesses = damage_relations['double_damage_from'].difference(
        damage_relations['half_damage_from'],
        damage_relations['no_damage_from']
    )
    
    strengths = damage_relations['double_damage_to'].difference(
        damage_relations['half_damage_to'],
        damage_relations['no_damage_to']
    )
    
    return {
        'weaknesses': sorted(weaknesses),
        'strengths': sorted(strengths)
    }

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def search_pokemon(request: Request, name: str = Form(...)):
    data = get_pokemon_data(name)
    if not data:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Pokemon not found!"
        })
    
    type_relations = process_type_relations(data['type_info'])
    
    result = {
        'name': data['pokemon']['name'].capitalize(),
        'id': data['pokemon']['id'],
        'image': data['pokemon']['sprites']['other']['official-artwork']['front_default'],
        'types': [t['type']['name'].capitalize() for t in data['pokemon']['types']],
        'stats': {stat['stat']['name'].capitalize(): stat['base_stat'] for stat in data['pokemon']['stats']},
        'height': data['pokemon']['height'] / 10,  # Convert to meters
        'weight': data['pokemon']['weight'] / 10,   # Convert to kg
        'abilities': [a['ability']['name'].capitalize() for a in data['pokemon']['abilities']],
        'description': next((flavor['flavor_text'] for flavor in data['species']['flavor_text_entries'] 
                            if flavor['language']['name'] == 'en'), None),
        'weaknesses': type_relations['weaknesses'],
        'strengths': type_relations['strengths']
    }
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result
    })