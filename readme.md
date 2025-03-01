# Pokedex with FastAPI

A web-based Pokedex built with FastAPI that retrieves and displays Pokemon information using the [PokeAPI](https://pokeapi.co/).

![Pokedex Screenshot](https://github.com/prasannakotyal/Pokedex/blob/master/outputs/charizard.png)

![Pokedex Screenshot](https://github.com/prasannakotyal/Pokedex/blob/master/outputs/mewtwo.png)

## Features

- Search any Pokemon by name
- Display official artwork
- View type strengths and weaknesses
- Show base stats and physical characteristics
- List abilities and descriptions
- Responsive design with Bulma CSS
- Error handling for invalid searches

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pokedex-fastapi.git
cd pokedex-fastapi
```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn main:app --reload
```

Visit http://localhost:8000 in your browser.

Usage
Enter a Pokemon name in the search box

View detailed information including:

- Type effectiveness

- Base stats

- Physical characteristics

- Abilities

- Official artwork

Example searches: "pikachu", "charizard", "mewtwo"