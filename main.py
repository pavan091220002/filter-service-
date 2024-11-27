from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
import json
from fastapi.middleware.cors import CORSMiddleware
from models import Category, Size, Color, SortBy, FashionItem, PaginatedResponse

app = FastAPI(title="Fashion Filter Service API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_mock_data(file_path: str) -> List[FashionItem]:
    fashion_items: List[FashionItem] = []

    try:
        with open(file_path, 'r') as json_file:
            mock_items = json.load(json_file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding JSON data")

    for item in mock_items:
        try:
            item['category'] = Category(item['category'])
            item['size'] = [Size(size) for size in item['size']]
            item['color'] = [Color(color) for color in item['color']]
            fashion_items.append(FashionItem(**item))
        except ValueError as e:
            raise HTTPException(status_code=500, detail=f"Error processing item data: {e}")

    return fashion_items

file_path = 'data_items.json'
try:
    fashion_items = load_mock_data(file_path)
except HTTPException as e:
    raise e

@app.get("/api/items", response_model=PaginatedResponse)
async def get_items(
    category: Optional[Category] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    size: Optional[Size] = None,
    color: Optional[Color] = None,
    designer: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    sort_by: Optional[SortBy] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(12, gt=0, le=100)
) -> PaginatedResponse:
    filtered_items = fashion_items.copy()

    if category:
        filtered_items = [item for item in filtered_items if item.category == category]

    if min_price is not None:
        filtered_items = [item for item in filtered_items if item.price >= min_price]

    if max_price is not None:
        filtered_items = [item for item in filtered_items if item.price <= max_price]

    if size:
        filtered_items = [item for item in filtered_items if size in item.size]

    if color:
        filtered_items = [item for item in filtered_items if color in item.color]

    if designer:
        filtered_items = [
            item for item in filtered_items
            if designer.lower() in item.designer.lower()
        ]

    if min_rating is not None:
        filtered_items = [item for item in filtered_items if item.rating >= min_rating]

    if sort_by:
        if sort_by == SortBy.PRICE_ASC:
            filtered_items.sort(key=lambda x: x.price)
        elif sort_by == SortBy.PRICE_DESC:
            filtered_items.sort(key=lambda x: x.price, reverse=True)
        elif sort_by == SortBy.RATING_DESC:
            filtered_items.sort(key=lambda x: x.rating, reverse=True)

    total_items = len(filtered_items)
    total_pages = (total_items + page_size - 1) // page_size

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = filtered_items[start_idx:end_idx]

    return PaginatedResponse(
        items=paginated_items,
        total=total_items,
        page=page,
        size=page_size,
        total_pages=total_pages
    )

@app.get("/api/items/{item_id}", response_model=FashionItem)
async def get_item(item_id: str) -> FashionItem:
    for item in fashion_items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/api/categories", response_model=PaginatedResponse)
async def get_categories(
    category: Optional[Category] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(12, gt=0, le=100)
) -> PaginatedResponse:
    if category:
        filtered_items = [item for item in fashion_items if item.category == category]
    else:
        filtered_items = fashion_items.copy()

    total_items = len(filtered_items)
    total_pages = (total_items + page_size - 1) // page_size

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = filtered_items[start_idx:end_idx]

    return PaginatedResponse(
        items=paginated_items,
        total=total_items,
        page=page,
        size=page_size,
        total_pages=total_pages
    )


@app.get("/api/sizes", response_model=PaginatedResponse)
async def get_sizes(
    size: Optional[Size] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(12, gt=0, le=100)
) -> PaginatedResponse:
    if size:
        filtered_items = [item for item in fashion_items if size in item.size]
    else:
        filtered_items = fashion_items.copy()

    total_items = len(filtered_items)
    total_pages = (total_items + page_size - 1) // page_size

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = filtered_items[start_idx:end_idx]

    return PaginatedResponse(
        items=paginated_items,
        total=total_items,
        page=page,
        size=page_size,
        total_pages=total_pages
    )

@app.get("/api/colors", response_model=PaginatedResponse)
async def get_colors(
    color: Optional[Color] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(12, gt=0, le=100)
) -> PaginatedResponse:
    if color:
        filtered_items = [item for item in fashion_items if color in item.color]
    else:
        filtered_items = fashion_items.copy()

    total_items = len(filtered_items)
    total_pages = (total_items + page_size - 1) // page_size

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = filtered_items[start_idx:end_idx]

    return PaginatedResponse(
        items=paginated_items,
        total=total_items,
        page=page,
        size=page_size,
        total_pages=total_pages
    )

@app.get("/api/designers", response_model=PaginatedResponse)
async def get_designers(
    designer: Optional[str] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(12, gt=0, le=100)
) -> PaginatedResponse:
    if designer:
        filtered_items = [item for item in fashion_items if designer.lower() in item.designer.lower()]
    else:
        filtered_items = fashion_items.copy()

    total_items = len(filtered_items)
    total_pages = (total_items + page_size - 1) // page_size

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="Page not found")

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_items = filtered_items[start_idx:end_idx]

    return PaginatedResponse(
        items=paginated_items,
        total=total_items,
        page=page,
        size=page_size,
        total_pages=total_pages
    )