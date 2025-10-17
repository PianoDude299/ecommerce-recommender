"""
LLM service for generating personalized product recommendation explanations.
Uses Google Gemini API.
"""

import google.generativeai as genai
from typing import Dict, Any, Optional
from app.config import get_settings
from app.models.database import Product, User

settings = get_settings()

# Configure Gemini API
genai.configure(api_key=settings.google_api_key)


class LLMExplanationService:
    """Service for generating LLM-powered recommendation explanations."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.model = genai.GenerativeModel(settings.llm_model)
        self.generation_config = genai.types.GenerationConfig(
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_tokens,
        )
    
    def generate_explanation(
        self,
        product: Product,
        user_insights: Dict[str, Any],
        recommendation_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a personalized explanation for why a product is recommended.
        
        Args:
            product: The recommended product
            user_insights: User behavior insights
            recommendation_context: Additional context (scores, algorithm used, etc.)
            
        Returns:
            Personalized explanation text
        """
        prompt = self._build_prompt(product, user_insights, recommendation_context)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            explanation = response.text.strip()
            
            # Fallback if response is too short or empty
            if len(explanation) < 20:
                explanation = self._generate_fallback_explanation(product, user_insights)
            
            return explanation
            
        except Exception as e:
            print(f"Error generating LLM explanation: {e}")
            return self._generate_fallback_explanation(product, user_insights)
    
    def _build_prompt(
        self,
        product: Product,
        user_insights: Dict[str, Any],
        recommendation_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build a detailed prompt for the LLM."""
        
        # Extract user preferences
        favorite_categories = [cat['category'] for cat in user_insights.get('favorite_categories', [])]
        favorite_brands = [brand['brand'] for brand in user_insights.get('favorite_brands', [])]
        avg_price = user_insights.get('avg_price', 0)
        recent_purchases = user_insights.get('recent_purchases', [])
        
        # Build context strings
        categories_str = ", ".join(favorite_categories) if favorite_categories else "various categories"
        brands_str = ", ".join(favorite_brands) if favorite_brands else "various brands"
        purchases_str = ", ".join([p['name'] for p in recent_purchases[:3]]) if recent_purchases else "no recent purchases"
        
        prompt = f"""You are a helpful e-commerce shopping assistant. Generate a personalized, persuasive explanation for why this product is recommended to the user.

USER BEHAVIOR SUMMARY:
- Total interactions: {user_insights.get('total_interactions', 0)}
- Favorite categories: {categories_str}
- Favorite brands: {brands_str}
- Average price range: ${avg_price:.2f}
- Recent purchases: {purchases_str}

RECOMMENDED PRODUCT:
- Name: {product.name}
- Category: {product.category}
- Brand: {product.brand}
- Price: ${product.price}
- Rating: {product.rating}/5.0
- Description: {product.description}
"""
        
        if product.attributes:
            attrs_str = ", ".join([f"{k}: {v}" for k, v in product.attributes.items()])
            prompt += f"- Key Features: {attrs_str}\n"
        
        if recommendation_context:
            score = recommendation_context.get('score', 0)
            prompt += f"\nRecommendation Score: {score:.2f}/1.00\n"
        
        prompt += """
TASK:
Write a 2-3 sentence personalized explanation for why this product is recommended. Be specific about how it matches the user's preferences and behavior. Make it conversational, persuasive, and data-driven.

GUIDELINES:
- Reference specific user preferences (categories, brands, price range)
- Highlight how the product matches their interests
- Keep it concise (40-60 words)
- Be enthusiastic but natural
- Don't use generic phrases

EXPLANATION:"""
        
        return prompt
    
    def _generate_fallback_explanation(
        self,
        product: Product,
        user_insights: Dict[str, Any]
    ) -> str:
        """Generate a simple rule-based explanation if LLM fails."""
        favorite_categories = user_insights.get('favorite_categories', [])
        favorite_brands = user_insights.get('favorite_brands', [])
        
        explanations = []
        
        # Category match
        if favorite_categories and product.category == favorite_categories[0]['category']:
            explanations.append(f"matches your interest in {product.category}")
        
        # Brand match
        if favorite_brands and product.brand in [b['brand'] for b in favorite_brands]:
            explanations.append(f"from {product.brand}, a brand you've shown preference for")
        
        # Rating
        if product.rating >= 4.5:
            explanations.append(f"has an excellent {product.rating}/5.0 rating")
        
        # Price match
        avg_price = user_insights.get('avg_price', 0)
        if avg_price > 0 and abs(product.price - avg_price) / avg_price < 0.3:
            explanations.append("fits your typical price range")
        
        if explanations:
            explanation_text = ", ".join(explanations[:2])
            return f"This {product.name} is recommended because it {explanation_text}."
        else:
            return f"This {product.name} is a highly-rated product in {product.category} that matches similar users' preferences."
    
    def batch_generate_explanations(
        self,
        recommendations: list[Dict[str, Any]],
        user_insights: Dict[str, Any]
    ) -> list[Dict[str, Any]]:
        """
        Generate explanations for multiple recommendations.
        
        Args:
            recommendations: List of recommendation dicts with product info
            user_insights: User behavior insights
            
        Returns:
            Updated recommendations with explanations added
        """
        for rec in recommendations:
            product = rec['product']
            context = {
                'score': rec.get('score', 0),
                'rank': rec.get('rank', 0),
                'algorithm_used': rec.get('algorithm_used', 'hybrid')
            }
            
            explanation = self.generate_explanation(
                product=product,
                user_insights=user_insights,
                recommendation_context=context
            )
            
            rec['explanation'] = explanation
        
        return recommendations