import React, { useState, useEffect } from 'react';
import { TrendingUp, Heart, DollarSign, Activity, Package } from 'lucide-react';
import { recommendationsApi } from '../services/api';
import { formatCurrency } from '../utils/helpers';
import LoadingSpinner from './LoadingSpinner';

const UserInsights = ({ userId }) => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (userId) {
      fetchInsights();
    }
  }, [userId]);

  const fetchInsights = async () => {
    setLoading(true);
    try {
      const response = await recommendationsApi.getUserInsights(userId);
      setInsights(response.data.insights);
    } catch (error) {
      console.error('Failed to fetch insights:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner size="sm" text="Loading insights..." />;
  }

  if (!insights) {
    return null;
  }

  return (
    <div className="space-y-4">
      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4">
        {/* Total Interactions */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-blue-600 font-medium">Interactions</p>
              <p className="text-2xl font-bold text-blue-900">
                {insights.total_interactions}
              </p>
            </div>
            <Activity className="h-8 w-8 text-blue-600" />
          </div>
        </div>

        {/* Purchases */}
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-green-600 font-medium">Purchases</p>
              <p className="text-2xl font-bold text-green-900">
                {insights.recent_purchases?.length || 0}
              </p>
            </div>
            <Package className="h-8 w-8 text-green-600" />
          </div>
        </div>

        {/* Average Price */}
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 border border-purple-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-purple-600 font-medium">Avg. Price</p>
              <p className="text-2xl font-bold text-purple-900">
                {formatCurrency(insights.avg_price || 0)}
              </p>
            </div>
            <DollarSign className="h-8 w-8 text-purple-600" />
          </div>
        </div>

        {/* Favorite Categories Count */}
        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-4 border border-orange-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-orange-600 font-medium">Categories</p>
              <p className="text-2xl font-bold text-orange-900">
                {insights.favorite_categories?.length || 0}
              </p>
            </div>
            <TrendingUp className="h-8 w-8 text-orange-600" />
          </div>
        </div>
      </div>

      {/* Favorite Categories */}
        {insights.favorite_categories && insights.favorite_categories.length > 0 && (
        <div className="card p-4">
            <div className="flex items-center space-x-2 mb-3">
            <Heart className="h-5 w-5 text-red-500" />
            <h3 className="font-semibold text-gray-900">Favorite Categories</h3>
            </div>
            <div className="space-y-3">
            {insights.favorite_categories.map((cat, idx) => {
                const maxCount = insights.favorite_categories[0].count;
                const percentage = (cat.count / maxCount) * 100;
                
                return (
                <div key={idx} className="space-y-1">
                    <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-700 font-medium">{cat.category}</span>
                    <span className="text-gray-900 font-semibold tabular-nums">
                        {Math.round(cat.count)}
                    </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
                    <div
                        className="bg-gradient-to-r from-primary-500 to-primary-600 h-2.5 rounded-full transition-all duration-500 ease-out"
                        style={{ width: `${percentage}%` }}
                    />
                    </div>
                </div>
                );
            })}
            </div>
        </div>
        )}

      {/* Favorite Brands */}
      {insights.favorite_brands && insights.favorite_brands.length > 0 && (
        <div className="card p-4">
          <h3 className="font-semibold text-gray-900 mb-3">Favorite Brands</h3>
          <div className="flex flex-wrap gap-2">
            {insights.favorite_brands.map((brand, idx) => (
              <span
                key={idx}
                className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium"
              >
                {brand.brand}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Recent Purchases */}
      {insights.recent_purchases && insights.recent_purchases.length > 0 && (
        <div className="card p-4">
          <h3 className="font-semibold text-gray-900 mb-3">Recent Purchases</h3>
          <div className="space-y-2">
            {insights.recent_purchases.slice(0, 3).map((purchase, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0"
              >
                <div>
                  <p className="text-sm font-medium text-gray-900 line-clamp-1">
                    {purchase.name}
                  </p>
                  <p className="text-xs text-gray-500">{purchase.category}</p>
                </div>
                <span className="text-sm font-semibold text-gray-900">
                  {formatCurrency(purchase.price)}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default UserInsights;