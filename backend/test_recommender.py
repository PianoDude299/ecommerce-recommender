"""Test script for the recommendation engine."""

from app.database import get_db
from app.services.recommender import RecommendationEngine
from app.services.llm_service import LLMExplanationService
from app.models.database import User
from app.config import get_settings

settings = get_settings()


def test_recommendations():
    """Test the recommendation engine with sample users."""
    db = next(get_db())
    
    try:
        print("\n" + "="*70)
        print("🧪 TESTING RECOMMENDATION ENGINE")
        print("="*70 + "\n")
        
        # Initialize services
        recommender = RecommendationEngine(
            db=db,
            collaborative_weight=settings.collaborative_weight,
            content_weight=settings.content_weight
        )
        llm_service = LLMExplanationService()
        
        # Get first user
        user = db.query(User).first()
        
        if not user:
            print("❌ No users found in database. Run seed_database.py first.")
            return
        
        print(f"👤 Testing recommendations for: {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Preferences: {user.preferences}\n")
        
        # Get user insights
        print("📊 Analyzing user behavior...")
        insights = recommender.get_user_insights(user.id)
        print(f"   Total interactions: {insights['total_interactions']}")
        print(f"   Favorite categories: {[c['category'] for c in insights['favorite_categories']]}")
        print(f"   Favorite brands: {[b['brand'] for b in insights['favorite_brands']]}")
        print(f"   Average price: ${insights['avg_price']}\n")
        
        # Generate recommendations
        print("🎯 Generating recommendations...\n")
        recommendations = recommender.get_recommendations(
            user_id=user.id,
            top_k=5,
            exclude_interacted=True
        )
        
        if not recommendations:
            print("   ⚠️  No recommendations generated. User may have interacted with all products.")
            return
        
        print(f"✅ Generated {len(recommendations)} recommendations:\n")
        print("="*70)
        
        # Display recommendations
        for rec in recommendations:
            product = rec['product']
            print(f"\n#{rec['rank']} {product.name}")
            print(f"   Category: {product.category} | Brand: {product.brand}")
            print(f"   Price: ${product.price} | Rating: {product.rating}⭐")
            print(f"   Score: {rec['score']:.4f} (Collab: {rec['collab_score']:.4f}, Content: {rec['content_score']:.4f})")
            
            # Generate explanation
            print(f"   🤖 Generating explanation...")
            explanation = llm_service.generate_explanation(
                product=product,
                user_insights=insights,
                recommendation_context=rec
            )
            print(f"   💬 {explanation}")
            print("   " + "-"*66)
        
        print("\n" + "="*70)
        print("✅ Recommendation engine test completed successfully!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_recommendations()