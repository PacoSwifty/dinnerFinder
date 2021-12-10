import datetime
from dataclasses import dataclass


@dataclass
class Recipe:
    id: str
    name: str
    url: str
    notes: str
    dateCooked: datetime.datetime
    coreIngredients: [str]
    cuisines: [str]
