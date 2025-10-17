from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    brand: Optional[str] = Field(None, max_length=100)
    attributes: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = Field(None, max_length=500)
    stock: int = Field(default=100, ge=0)
    rating: float = Field(default=0.0, ge=0, le=5)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# User Schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    preferences: Optional[Dict[str, Any]] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Interaction Schemas
class InteractionBase(BaseModel):
    user_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    interaction_type: str = Field(..., pattern="^(view|click|cart|purchase|rating)$")
    duration: Optional[int] = Field(None, ge=0)
    rating: Optional[float] = Field(None, ge=0, le=5)
    context: Optional[Dict[str, Any]] = None


class InteractionCreate(InteractionBase):
    pass


class InteractionResponse(InteractionBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationBase(BaseModel):
    product_id: int
    score: float
    algorithm_used: str
    explanation: Optional[str] = None
    rank: int


class RecommendationResponse(RecommendationBase):
    id: int
    user_id: int
    product: ProductResponse
    created_at: datetime
    
    class Config:
        from_attributes = True


class RecommendationRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    limit: int = Field(default=10, gt=0, le=50)
    include_explanation: bool = Field(default=True)


class RecommendationListResponse(BaseModel):
    user_id: int
    recommendations: List[RecommendationResponse]
    total_count: int
    generated_at: datetime


# Explanation Request Schema
class ExplanationRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    user_behavior_summary: Optional[str] = None


class ExplanationResponse(BaseModel):
    product_id: int
    user_id: int
    explanation: str
    generated_at: datetime


# User Insights Schema
class UserInsights(BaseModel):
    user_id: int
    total_interactions: int
    favorite_categories: List[Dict[str, Any]]
    recent_activity: List[InteractionResponse]
    average_rating: Optional[float]
    purchase_count: int
    
    class Config:
        from_attributes = True