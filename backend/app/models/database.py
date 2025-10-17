from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from typing import Optional

Base = declarative_base()


class Product(Base):
    """Product model for storing product information."""
    
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    price = Column(Float, nullable=False)
    brand = Column(String(100), nullable=True)
    attributes = Column(JSON, nullable=True)  # Store additional attributes as JSON
    image_url = Column(String(500), nullable=True)
    stock = Column(Integer, default=100)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interactions = relationship("Interaction", back_populates="product", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', category='{self.category}')>"


class User(Base):
    """User model for storing user information."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    preferences = Column(JSON, nullable=True)  # Store user preferences as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    interactions = relationship("Interaction", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"


class Interaction(Base):
    """Interaction model for tracking user-product interactions."""
    
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    interaction_type = Column(String(50), nullable=False)  # view, click, cart, purchase
    duration = Column(Integer, nullable=True)  # Time spent in seconds
    rating = Column(Float, nullable=True)  # User rating if applicable
    context = Column(JSON, nullable=True)  # Additional context (search query, etc.)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="interactions")
    product = relationship("Product", back_populates="interactions")
    
    def __repr__(self):
        return f"<Interaction(user_id={self.user_id}, product_id={self.product_id}, type='{self.interaction_type}')>"


class Recommendation(Base):
    """Recommendation model for storing generated recommendations."""
    
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    score = Column(Float, nullable=False)  # Recommendation confidence score
    algorithm_used = Column(String(100), nullable=False)  # collaborative, content-based, hybrid
    explanation = Column(Text, nullable=True)  # LLM-generated explanation
    rank = Column(Integer, nullable=False)  # Position in recommendation list
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    product = relationship("Product", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation(user_id={self.user_id}, product_id={self.product_id}, score={self.score:.2f})>"