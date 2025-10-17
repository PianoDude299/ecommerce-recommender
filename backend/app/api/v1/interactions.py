"""
Interactions API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.database import Interaction, User, Product
from app.models.schemas import InteractionCreate, InteractionResponse

router = APIRouter(prefix="/interactions", tags=["interactions"])


@router.post("/", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED)
def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db)
):
    """Create a new user-product interaction."""
    # Verify user exists
    user = db.query(User).filter(User.id == interaction.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {interaction.user_id} not found"
        )
    
    # Verify product exists
    product = db.query(Product).filter(Product.id == interaction.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {interaction.product_id} not found"
        )
    
    try:
        db_interaction = Interaction(**interaction.model_dump())
        db.add(db_interaction)
        db.commit()
        db.refresh(db_interaction)
        return db_interaction
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create interaction: {str(e)}"
        )


@router.get("/user/{user_id}", response_model=List[InteractionResponse])
def get_user_interactions(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all interactions for a specific user."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    interactions = db.query(Interaction).filter(
        Interaction.user_id == user_id
    ).order_by(
        Interaction.timestamp.desc()
    ).offset(skip).limit(limit).all()
    
    return interactions


@router.get("/product/{product_id}", response_model=List[InteractionResponse])
def get_product_interactions(
    product_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all interactions for a specific product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    
    interactions = db.query(Interaction).filter(
        Interaction.product_id == product_id
    ).order_by(
        Interaction.timestamp.desc()
    ).offset(skip).limit(limit).all()
    
    return interactions