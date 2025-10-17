"""
Hybrid recommendation engine combining collaborative and content-based filtering.
"""

from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.models.database import Product, User, Interaction
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict, Counter
from sklearn.metrics.pairwise import cosine_similarity
import json


class RecommendationEngine:
    """Hybrid recommendation engine for e-commerce products."""
    
    def __init__(
        self,
        db: Session,
        collaborative_weight: float = 0.6,
        content_weight: float = 0.4,
        recency_days: int = 30
    ):
        """
        Initialize the recommendation engine.
        
        Args:
            db: Database session
            collaborative_weight: Weight for collaborative filtering (0-1)
            content_weight: Weight for content-based filtering (0-1)
            recency_days: Number of days to consider for recent interactions
        """
        self.db = db
        self.collaborative_weight = collaborative_weight
        self.content_weight = content_weight
        self.recency_days = recency_days
        
        # Interaction type weights (how much each interaction type matters)
        self.interaction_weights = {
            'view': 1.0,
            'click': 2.0,
            'cart': 3.0,
            'purchase': 5.0,
            'rating': 4.0
        }
    
    def get_recommendations(
        self,
        user_id: int,
        top_k: int = 10,
        exclude_interacted: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate hybrid recommendations for a user.
        
        Args:
            user_id: User ID to generate recommendations for
            top_k: Number of recommendations to return
            exclude_interacted: Whether to exclude already interacted products
            
        Returns:
            List of recommended products with scores and metadata
        """
        # Get user interactions
        user_interactions = self._get_user_interactions(user_id)
        
        if not user_interactions:
            # Cold start: return popular products
            return self._get_popular_products(top_k)
        
        # Get all products
        all_products = self.db.query(Product).all()
        product_ids = [p.id for p in all_products]
        
        # Calculate collaborative filtering scores
        collab_scores = self._collaborative_filtering(user_id, product_ids)
        
        # Calculate content-based filtering scores
        content_scores = self._content_based_filtering(user_id, product_ids, user_interactions)
        
        # Combine scores using weighted ensemble
        hybrid_scores = self._combine_scores(collab_scores, content_scores)
        
        # Exclude already interacted products if requested
        if exclude_interacted:
            interacted_product_ids = set(i['product_id'] for i in user_interactions)
            hybrid_scores = {
                pid: score for pid, score in hybrid_scores.items()
                if pid not in interacted_product_ids
            }
        
        # Sort by score and get top K
        sorted_products = sorted(
            hybrid_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
        
        # Apply diversity filter to avoid same-category dominance
        diverse_products = self._apply_diversity_filter(sorted_products, max_per_category=3)
        
        # Build recommendation results
        recommendations = []
        for rank, (product_id, score) in enumerate(diverse_products, 1):
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if product:
                recommendations.append({
                    'product_id': product_id,
                    'product': product,
                    'score': round(score, 4),
                    'rank': rank,
                    'algorithm_used': 'hybrid',
                    'collab_score': round(collab_scores.get(product_id, 0), 4),
                    'content_score': round(content_scores.get(product_id, 0), 4)
                })
        
        return recommendations
    
    def _get_user_interactions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's interaction history with recency weighting."""
        cutoff_date = datetime.utcnow() - timedelta(days=self.recency_days)
        
        interactions = self.db.query(Interaction).filter(
            and_(
                Interaction.user_id == user_id,
                Interaction.timestamp >= cutoff_date
            )
        ).order_by(Interaction.timestamp.desc()).all()
        
        # Convert to dict format with recency weights
        result = []
        for interaction in interactions:
            days_ago = (datetime.utcnow() - interaction.timestamp).days
            recency_weight = 1.0 / (1.0 + days_ago * 0.1)  # Decay over time
            
            result.append({
                'product_id': interaction.product_id,
                'interaction_type': interaction.interaction_type,
                'weight': self.interaction_weights[interaction.interaction_type] * recency_weight,
                'timestamp': interaction.timestamp,
                'rating': interaction.rating
            })
        
        return result
    
    def _collaborative_filtering(
        self,
        user_id: int,
        product_ids: List[int]
    ) -> Dict[int, float]:
        """
        Collaborative filtering based on user similarity.
        Users who interacted with similar products will have similar recommendations.
        """
        # Build user-product interaction matrix
        user_product_matrix = self._build_user_product_matrix()
        
        if user_id not in user_product_matrix:
            return {pid: 0.0 for pid in product_ids}
        
        # Find similar users
        similar_users = self._find_similar_users(user_id, user_product_matrix)
        
        # Aggregate scores from similar users
        scores = defaultdict(float)
        target_user_products = set(user_product_matrix[user_id].keys())
        
        for similar_user_id, similarity in similar_users:
            similar_user_products = user_product_matrix[similar_user_id]
            
            for product_id, weight in similar_user_products.items():
                # Skip products the target user has already interacted with
                if product_id not in target_user_products:
                    scores[product_id] += weight * similarity
        
        # Normalize scores
        if scores:
            max_score = max(scores.values())
            if max_score > 0:
                scores = {pid: score / max_score for pid, score in scores.items()}
        
        # Ensure all product IDs are in the result
        return {pid: scores.get(pid, 0.0) for pid in product_ids}
    
    def _content_based_filtering(
        self,
        user_id: int,
        product_ids: List[int],
        user_interactions: List[Dict[str, Any]]
    ) -> Dict[int, float]:
        """
        Content-based filtering based on product attributes.
        Recommend products similar to what the user has interacted with.
        """
        if not user_interactions:
            return {pid: 0.0 for pid in product_ids}
        
        # Build user profile from interactions
        user_profile = self._build_user_profile(user_interactions)
        
        # Calculate similarity scores for each product
        scores = {}
        for product_id in product_ids:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if product:
                similarity = self._calculate_product_similarity(product, user_profile)
                scores[product_id] = similarity
        
        # Normalize scores
        if scores:
            max_score = max(scores.values())
            if max_score > 0:
                scores = {pid: score / max_score for pid, score in scores.items()}
        
        return scores
    
    def _build_user_product_matrix(self) -> Dict[int, Dict[int, float]]:
        """Build a user-product interaction matrix with weighted interactions."""
        matrix = defaultdict(lambda: defaultdict(float))
        
        cutoff_date = datetime.utcnow() - timedelta(days=self.recency_days)
        interactions = self.db.query(Interaction).filter(
            Interaction.timestamp >= cutoff_date
        ).all()
        
        for interaction in interactions:
            days_ago = (datetime.utcnow() - interaction.timestamp).days
            recency_weight = 1.0 / (1.0 + days_ago * 0.1)
            
            weight = self.interaction_weights[interaction.interaction_type] * recency_weight
            matrix[interaction.user_id][interaction.product_id] += weight
        
        return dict(matrix)
    
    def _find_similar_users(
        self,
        user_id: int,
        user_product_matrix: Dict[int, Dict[int, float]],
        top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """Find K most similar users using cosine similarity."""
        if user_id not in user_product_matrix:
            return []
        
        target_user_vector = user_product_matrix[user_id]
        similarities = []
        
        for other_user_id, other_user_vector in user_product_matrix.items():
            if other_user_id == user_id:
                continue
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(target_user_vector, other_user_vector)
            if similarity > 0:
                similarities.append((other_user_id, similarity))
        
        # Sort by similarity and return top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def _cosine_similarity(
        self,
        vector1: Dict[int, float],
        vector2: Dict[int, float]
    ) -> float:
        """Calculate cosine similarity between two sparse vectors."""
        # Get common products
        common_products = set(vector1.keys()) & set(vector2.keys())
        
        if not common_products:
            return 0.0
        
        # Calculate dot product and magnitudes
        dot_product = sum(vector1[pid] * vector2[pid] for pid in common_products)
        
        magnitude1 = np.sqrt(sum(v ** 2 for v in vector1.values()))
        magnitude2 = np.sqrt(sum(v ** 2 for v in vector2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _build_user_profile(self, user_interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build a user profile from their interaction history."""
        profile = {
            'categories': Counter(),
            'brands': Counter(),
            'price_range': [],
            'attributes': Counter()
        }
        
        for interaction in user_interactions:
            product = self.db.query(Product).filter(
                Product.id == interaction['product_id']
            ).first()
            
            if product:
                weight = interaction['weight']
                
                # Category preferences
                profile['categories'][product.category] += weight
                
                # Brand preferences
                if product.brand:
                    profile['brands'][product.brand] += weight
                
                # Price range
                profile['price_range'].append(product.price)
                
                # Attribute preferences
                if product.attributes:
                    for key, value in product.attributes.items():
                        profile['attributes'][f"{key}:{value}"] += weight
        
        # Calculate average price
        if profile['price_range']:
            profile['avg_price'] = np.mean(profile['price_range'])
            profile['price_std'] = np.std(profile['price_range'])
        else:
            profile['avg_price'] = 0
            profile['price_std'] = 0
        
        return profile
    
    def _calculate_product_similarity(
        self,
        product: Product,
        user_profile: Dict[str, Any]
    ) -> float:
        """Calculate similarity between a product and user profile."""
        similarity_score = 0.0
        
        # Category similarity (40% weight)
        if product.category in user_profile['categories']:
            category_weight = user_profile['categories'][product.category]
            total_category_weight = sum(user_profile['categories'].values())
            similarity_score += 0.4 * (category_weight / total_category_weight)
        
        # Brand similarity (20% weight)
        if product.brand and product.brand in user_profile['brands']:
            brand_weight = user_profile['brands'][product.brand]
            total_brand_weight = sum(user_profile['brands'].values())
            similarity_score += 0.2 * (brand_weight / total_brand_weight)
        
        # Price similarity (20% weight)
        if user_profile['avg_price'] > 0:
            price_diff = abs(product.price - user_profile['avg_price'])
            price_similarity = 1.0 / (1.0 + price_diff / user_profile['avg_price'])
            similarity_score += 0.2 * price_similarity
        
        # Attribute similarity (20% weight)
        if product.attributes and user_profile['attributes']:
            matching_attrs = 0
            total_attrs = len(user_profile['attributes'])
            
            for key, value in product.attributes.items():
                attr_key = f"{key}:{value}"
                if attr_key in user_profile['attributes']:
                    matching_attrs += 1
            
            if total_attrs > 0:
                similarity_score += 0.2 * (matching_attrs / total_attrs)
        
        return similarity_score
    
    def _combine_scores(
        self,
        collab_scores: Dict[int, float],
        content_scores: Dict[int, float]
    ) -> Dict[int, float]:
        """Combine collaborative and content-based scores using weighted average."""
        combined = {}
        all_product_ids = set(collab_scores.keys()) | set(content_scores.keys())
        
        for product_id in all_product_ids:
            collab = collab_scores.get(product_id, 0.0)
            content = content_scores.get(product_id, 0.0)
            
            combined[product_id] = (
                self.collaborative_weight * collab +
                self.content_weight * content
            )
        
        return combined
    
    def _apply_diversity_filter(
        self,
        sorted_products: List[Tuple[int, float]],
        max_per_category: int = 3
    ) -> List[Tuple[int, float]]:
        """Apply diversity filter to avoid recommending too many products from same category."""
        category_counts = defaultdict(int)
        diverse_products = []
        
        for product_id, score in sorted_products:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            
            if product:
                if category_counts[product.category] < max_per_category:
                    diverse_products.append((product_id, score))
                    category_counts[product.category] += 1
        
        return diverse_products
    
    def _get_popular_products(self, top_k: int) -> List[Dict[str, Any]]:
        """Get popular products for cold start scenarios."""
        # Get products with most interactions in last 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=self.recency_days)
        
        popular = self.db.query(
            Product.id,
            func.count(Interaction.id).label('interaction_count'),
            func.avg(Product.rating).label('avg_rating')
        ).join(Interaction).filter(
            Interaction.timestamp >= cutoff_date
        ).group_by(Product.id).order_by(
            func.count(Interaction.id).desc()
        ).limit(top_k).all()
        
        recommendations = []
        for rank, (product_id, interaction_count, avg_rating) in enumerate(popular, 1):
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if product:
                recommendations.append({
                    'product_id': product_id,
                    'product': product,
                    'score': 1.0 - (rank * 0.05),  # Decreasing score by rank
                    'rank': rank,
                    'algorithm_used': 'popularity',
                    'collab_score': 0.0,
                    'content_score': 0.0
                })
        
        return recommendations
    
    def get_user_insights(self, user_id: int) -> Dict[str, Any]:
        """Get insights about a user's behavior for explanation generation."""
        user_interactions = self._get_user_interactions(user_id)
        
        if not user_interactions:
            return {
                'total_interactions': 0,
                'favorite_categories': [],
                'favorite_brands': [],
                'avg_price': 0,
                'recent_purchases': []
            }
        
        # Build profile
        profile = self._build_user_profile(user_interactions)
        
        # Get top categories
        favorite_categories = [
            {'category': cat, 'count': count}
            for cat, count in profile['categories'].most_common(3)
        ]
        
        # Get top brands
        favorite_brands = [
            {'brand': brand, 'count': count}
            for brand, count in profile['brands'].most_common(3)
        ]
        
        # Get recent purchases
        recent_purchases = []
        for interaction in user_interactions:
            if interaction['interaction_type'] == 'purchase':
                product = self.db.query(Product).filter(
                    Product.id == interaction['product_id']
                ).first()
                if product:
                    recent_purchases.append({
                        'name': product.name,
                        'category': product.category,
                        'price': product.price
                    })
        
        return {
            'total_interactions': len(user_interactions),
            'favorite_categories': favorite_categories,
            'favorite_brands': favorite_brands,
            'avg_price': round(profile['avg_price'], 2) if profile['avg_price'] else 0,
            'recent_purchases': recent_purchases[:5]
        }