from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

class Category(str, Enum):
    DRESSES = "dresses"
    SHOES = "shoes"
    ACCESSORIES = "accessories"
    BAGS = "bags"
    JEWELRY = "jewelry"
    JACKETS = "jackets"
    TOPS = "tops"
    BOTTOMS = "bottoms"
    SLEEPWEAR = "sleepwear"
    
class Size(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

class Color(str, Enum):
    BLACK = "black"
    WHITE = "white"
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    PINK = "pink"
    PURPLE = "purple"
    GOLD = "gold"
    NAVY = "navy"
    MULTI = "multi"
    GRAY = "gray"
    BEIGE = "beige"
    BURGUNDY = "burgundy"
    

class SortBy(str, Enum):
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    RATING_DESC = "rating_desc"

class FashionItem(BaseModel):
    id: str
    name: str
    category: Category
    price: float = Field(gt=0)
    size: List[Size]
    color: List[Color]
    designer: str
    rating: float = Field(ge=0, le=5)
    
class PaginatedResponse(BaseModel):
    items: List[FashionItem]
    total: int
    page: int
    size: int
    total_pages: int
    
