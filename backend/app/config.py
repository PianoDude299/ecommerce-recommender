from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings and configuration."""
    
    # Google Gemini API
    google_api_key: str
    
    # Database
    database_url: str = "sqlite:///./ecommerce.db"
    
    # API Configuration
    api_v1_prefix: str = "/api/v1"
    project_name: str = "E-commerce Product Recommender"
    debug: bool = True
    
    # Recommendation Settings
    top_k_recommendations: int = 10
    collaborative_weight: float = 0.6
    content_weight: float = 0.4
    
    # LLM Settings
    llm_model: str = "gemini-2.0-flash-exp"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 200
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()