"""
Recommendations API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.database import User, Recommendation as DBRecommendation
from app.models.schemas import RecommendationRequest, RecommendationListResponse, RecommendationResponse
from app.services.recommender import RecommendationEngine
from app.services.llm_service import LLMExplanationService
from app.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/generate", response_model=RecommendationListResponse)
def generate_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Generate personalized recommendations for a user.
    
    This endpoint:
    1. Verifies the user exists
    2. Generates recommendations using the hybrid algorithm
    3. Optionally generates LLM explanations
    4. Stores recommendations in the database
    5. Returns the full recommendation list
    """
    # Verify user exists
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {request.user_id} not found"
        )
    
    try:
        # Initialize recommendation engine
        recommender = RecommendationEngine(
            db=db,
            collaborative_weight=settings.collaborative_weight,
            content_weight=settings.content_weight
        )
        
        # Generate recommendations
        recommendations = recommender.get_recommendations(
            user_id=request.user_id,
            top_k=request.limit,
            exclude_interacted=True
        )
        
        # Get user insights for explanations
        user_insights = recommender.get_user_insights(request.user_id)
        
        # Generate LLM explanations if requested
        if request.include_explanation:
            llm_service = LLMExplanationService()
            recommendations = llm_service.batch_generate_explanations(
                recommendations=recommendations,
                user_insights=user_insights
            )
        
        # Store recommendations in database
        db_recommendations = []
        for rec in recommendations:
            db_rec = DBRecommendation(
                user_id=request.user_id,
                product_id=rec['product_id'],
                score=rec['score'],
                algorithm_used=rec['algorithm_used'],
                explanation=rec.get('explanation'),
                rank=rec['rank']
            )
            db.add(db_rec)
            db_recommendations.append(db_rec)
        
        db.commit()
        
        # Refresh to get IDs and timestamps
        for db_rec in db_recommendations:
            db.refresh(db_rec)
        
        # Build response
        response = RecommendationListResponse(
            user_id=request.user_id,
            recommendations=[
                RecommendationResponse(
                    id=db_rec.id,
                    user_id=db_rec.user_id,
                    product_id=db_rec.product_id,
                    product=db_rec.product,
                    score=db_rec.score,
                    algorithm_used=db_rec.algorithm_used,
                    explanation=db_rec.explanation,
                    rank=db_rec.rank,
                    created_at=db_rec.created_at
                )
                for db_rec in db_recommendations
            ],
            total_count=len(db_recommendations),
            generated_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/{user_id}", response_model=RecommendationListResponse)
def get_user_recommendations(
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get the most recent stored recommendations for a user.
    
    This returns previously generated recommendations from the database.
    To generate fresh recommendations, use the /generate endpoint.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Get most recent recommendations
    recommendations = db.query(DBRecommendation).filter(
        DBRecommendation.user_id == user_id
    ).order_by(
        DBRecommendation.created_at.desc()
    ).limit(limit).all()
    
    if not recommendations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No recommendations found for user {user_id}. Use /generate to create new recommendations."
        )
    
    response = RecommendationListResponse(
        user_id=user_id,
        recommendations=[
            RecommendationResponse(
                id=rec.id,
                user_id=rec.user_id,
                product_id=rec.product_id,
                product=rec.product,
                score=rec.score,
                algorithm_used=rec.algorithm_used,
                explanation=rec.explanation,
                rank=rec.rank,
                created_at=rec.created_at
            )
            for rec in recommendations
        ],
        total_count=len(recommendations),
        generated_at=recommendations[0].created_at if recommendations else datetime.utcnow()
    )
    
    return response


@router.get("/insights/{user_id}")
def get_user_insights(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get behavioral insights for a user.
    
    Returns information about the user's interaction patterns,
    favorite categories, brands, and price preferences.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    try:
        recommender = RecommendationEngine(db=db)
        insights = recommender.get_user_insights(user_id)
        
        return {
            "user_id": user_id,
            "user_name": user.name,
            "insights": insights
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user insights: {str(e)}"
        )