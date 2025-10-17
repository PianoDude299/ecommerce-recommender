"""
Main API v1 router that combines all endpoint routers.
"""

from fastapi import APIRouter
from app.api.v1 import products, users, interactions, recommendations

api_router = APIRouter()

# Include all routers
api_router.include_router(products.router)
api_router.include_router(users.router)
api_router.include_router(interactions.router)
api_router.include_router(recommendations.router)