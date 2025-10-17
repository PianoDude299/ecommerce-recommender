import React from 'react';
import { Sparkles, TrendingUp } from 'lucide-react';
import ProductCard from './ProductCard';
import { getScoreColor } from '../utils/helpers';

const RecommendationCard = ({ 
  recommendation, 
  onView, 
  onAddToCart,
  showExplanation = true 
}) => {
  const { product, score, rank, explanation, algorithm_used } = recommendation;

  return (
    <div className="relative">
      {/* Rank Badge */}
      <div className="absolute -top-2 -left-2 z-10 bg-primary-600 text-white rounded-full h-8 w-8 flex items-center justify-center font-bold text-sm shadow-lg">
        #{rank}
      </div>

      {/* Score Badge */}
      <div className="absolute -top-2 -right-2 z-10">
        <div className={`${getScoreColor(score)} px-3 py-1 rounded-full text-xs font-semibold shadow-lg flex items-center space-x-1`}>
          <TrendingUp className="h-3 w-3" />
          <span>{(score * 100).toFixed(0)}%</span>
        </div>
      </div>

      {/* Product Card */}
      <div className="pt-2">
        <ProductCard
          product={product}
          onView={onView}
          onAddToCart={onAddToCart}
        />
      </div>

      {/* Explanation */}
      {showExplanation && explanation && (
        <div className="mt-3 p-4 bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg border border-primary-100">
          <div className="flex items-start space-x-2">
            <Sparkles className="h-5 w-5 text-primary-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm font-medium text-primary-900 mb-1">
                Why this recommendation?
              </p>
              <p className="text-sm text-gray-700 leading-relaxed">
                {explanation}
              </p>
              <p className="text-xs text-gray-500 mt-2">
                Algorithm: {algorithm_used}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecommendationCard;