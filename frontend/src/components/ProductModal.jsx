import React from 'react';
import { X, Star, StarHalf, Tag, Package } from 'lucide-react';
import { formatCurrency, getRatingStars } from '../utils/helpers';
import InteractionSimulator from './InteractionSimulator';

const ProductModal = ({ product, userId, isOpen, onClose, onInteractionCreated }) => {
  if (!isOpen || !product) return null;

  const { full, half, empty } = getRatingStars(product.rating);

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 animate-fade-in"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto animate-slide-up">
          {/* Header */}
          <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">Product Details</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <X className="h-6 w-6 text-gray-600" />
            </button>
          </div>

          {/* Content */}
          <div className="p-6">
            <div className="grid md:grid-cols-2 gap-8">
              {/* Left Column - Image */}
              <div>
                <div className="aspect-square bg-gray-100 rounded-xl overflow-hidden mb-4">
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-cover"
                  />
                </div>

                {/* Interaction Simulator */}
                <InteractionSimulator
                  userId={userId}
                  productId={product.id}
                  onInteractionCreated={onInteractionCreated}
                />
              </div>

              {/* Right Column - Details */}
              <div className="space-y-6">
                {/* Category & Brand */}
                <div className="flex items-center space-x-3">
                  <span className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium">
                    {product.category}
                  </span>
                  <span className="text-gray-600 text-sm">{product.brand}</span>
                </div>

                {/* Product Name */}
                <div>
                  <h1 className="text-3xl font-bold text-gray-900 mb-2">
                    {product.name}
                  </h1>

                  {/* Rating */}
                  <div className="flex items-center space-x-2">
                    <div className="flex items-center">
                      {[...Array(full)].map((_, i) => (
                        <Star key={`full-${i}`} className="h-5 w-5 fill-yellow-400 text-yellow-400" />
                      ))}
                      {half > 0 && <StarHalf className="h-5 w-5 fill-yellow-400 text-yellow-400" />}
                      {[...Array(empty)].map((_, i) => (
                        <Star key={`empty-${i}`} className="h-5 w-5 text-gray-300" />
                      ))}
                    </div>
                    <span className="text-lg font-semibold text-gray-900">
                      {product.rating}
                    </span>
                    <span className="text-gray-500">/ 5.0</span>
                  </div>
                </div>

                {/* Price */}
                <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-xl p-6 border border-primary-100">
                  <p className="text-sm text-gray-600 mb-1">Price</p>
                  <p className="text-4xl font-bold text-primary-600">
                    {formatCurrency(product.price)}
                  </p>
                </div>

                {/* Description */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                  <p className="text-gray-700 leading-relaxed">
                    {product.description}
                  </p>
                </div>

                {/* Attributes */}
                {product.attributes && Object.keys(product.attributes).length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-3">Specifications</h3>
                    <div className="grid grid-cols-2 gap-3">
                      {Object.entries(product.attributes).map(([key, value]) => (
                        <div key={key} className="bg-gray-50 rounded-lg p-3">
                          <p className="text-xs text-gray-500 uppercase mb-1">
                            {key.replace(/_/g, ' ')}
                          </p>
                          <p className="font-medium text-gray-900">
                            {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Stock Info */}
                <div className="flex items-center space-x-4 text-sm">
                  <div className="flex items-center space-x-2">
                    <Package className="h-5 w-5 text-gray-500" />
                    <span className="text-gray-700">
                      <span className="font-semibold">{product.stock}</span> in stock
                    </span>
                  </div>
                  {product.stock < 50 && (
                    <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-xs font-medium">
                      Low Stock
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default ProductModal;