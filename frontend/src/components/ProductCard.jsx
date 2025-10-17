import React from 'react';
import { Star, StarHalf, ShoppingCart, Eye } from 'lucide-react';
import { formatCurrency, getRatingStars } from '../utils/helpers';

const ProductCard = ({ product, onView, onAddToCart, showActions = true }) => {
  const { full, half, empty } = getRatingStars(product.rating);

  return (
    <div className="card p-4 group cursor-pointer" onClick={onView}>
      {/* Product Image */}
      <div className="relative overflow-hidden rounded-lg mb-4 bg-gray-100 aspect-square">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        {product.stock < 50 && (
          <span className="absolute top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
            Low Stock
          </span>
        )}
      </div>

      {/* Product Info */}
      <div className="space-y-2">
        {/* Category & Brand */}
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span className="bg-gray-100 px-2 py-1 rounded">{product.category}</span>
          <span>{product.brand}</span>
        </div>

        {/* Product Name */}
        <h3 className="font-semibold text-gray-900 line-clamp-2 min-h-[2.5rem]">
          {product.name}
        </h3>

        {/* Rating */}
        <div className="flex items-center space-x-1">
          {[...Array(full)].map((_, i) => (
            <Star key={`full-${i}`} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
          ))}
          {half > 0 && <StarHalf className="h-4 w-4 fill-yellow-400 text-yellow-400" />}
          {[...Array(empty)].map((_, i) => (
            <Star key={`empty-${i}`} className="h-4 w-4 text-gray-300" />
          ))}
          <span className="text-sm text-gray-600 ml-1">({product.rating})</span>
        </div>

        {/* Price */}
        <div className="flex items-center justify-between">
          <span className="text-2xl font-bold text-primary-600">
            {formatCurrency(product.price)}
          </span>
          {showActions && (
            <div className="flex space-x-2">
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onView?.();
                }}
                className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                title="View details"
              >
                <Eye className="h-5 w-5 text-gray-600" />
              </button>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onAddToCart?.();
                }}
                className="p-2 hover:bg-primary-100 rounded-full transition-colors"
                title="Add to cart"
              >
                <ShoppingCart className="h-5 w-5 text-primary-600" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;