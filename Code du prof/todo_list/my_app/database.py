from datetime import date
from uuid import uuid4


database = {
    "tasks": [
        {
            "id": str(uuid4()),
            "name": "Faire mon exercice de techno-web !",
            "description": "Il ne faut pas que j'oublie de soumettre mon exercice pratique avant la deadline !",
            "creation_date": date(year=2024, month=1, day=21),
        },
        {
            "id": str(uuid4()),
            "name": "Sortir le chien",
            "description": "N'oublions pas de sortir Kiki, le pauvre !",
            "creation_date": date(year=2024, month=1, day=15),
        },
        {
            "id": str(uuid4()),
            "name": "Rendre les cartes pokemons à Titouan",
            "description": "Il a peut être oublié mais bon...",
            "creation_date": date(year=2023, month=12, day=27),
        },
        {
            "id": str(uuid4()),
            "name": "Remplacer l'ampoule dans le salon",
            "description": "",
            "creation_date": date(year=2023, month=12, day=21),
        },
    ]
}
