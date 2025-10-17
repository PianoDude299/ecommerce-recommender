import React, { useState } from 'react';
import { MousePointer, ShoppingCart, Eye, CreditCard, Star } from 'lucide-react';
import { interactionsApi } from '../services/api';

const InteractionSimulator = ({ userId, productId, onInteractionCreated }) => {
  const [creating, setCreating] = useState(false);
  const [message, setMessage] = useState(null);

  const interactionTypes = [
    { type: 'view', label: 'View', icon: Eye, color: 'bg-gray-100 hover:bg-gray-200 text-gray-700' },
    { type: 'click', label: 'Click', icon: MousePointer, color: 'bg-blue-100 hover:bg-blue-200 text-blue-700' },
    { type: 'cart', label: 'Add to Cart', icon: ShoppingCart, color: 'bg-yellow-100 hover:bg-yellow-200 text-yellow-700' },
    { type: 'purchase', label: 'Purchase', icon: CreditCard, color: 'bg-green-100 hover:bg-green-200 text-green-700' },
    { type: 'rating', label: 'Rate 5★', icon: Star, color: 'bg-purple-100 hover:bg-purple-200 text-purple-700' },
  ];

  const handleInteraction = async (interactionType) => {
    if (!userId || !productId) {
      setMessage({ type: 'error', text: 'Please select a user and product' });
      setTimeout(() => setMessage(null), 3000);
      return;
    }

    setCreating(true);
    try {
      const interactionData = {
        user_id: userId,
        product_id: productId,
        interaction_type: interactionType,
      };

      // Add duration for views (random 10-120 seconds)
      if (interactionType === 'view') {
        interactionData.duration = Math.floor(Math.random() * 110) + 10;
      }

      // Add rating for rating interactions
      if (interactionType === 'rating') {
        interactionData.rating = 5.0;
      }

      await interactionsApi.create(interactionData);
      
      setMessage({ 
        type: 'success', 
        text: `${interactionType.charAt(0).toUpperCase() + interactionType.slice(1)} recorded!` 
      });
      
      setTimeout(() => setMessage(null), 3000);
      
      if (onInteractionCreated) {
        onInteractionCreated();
      }
    } catch (error) {
      console.error('Failed to create interaction:', error);
      setMessage({ type: 'error', text: 'Failed to record interaction' });
      setTimeout(() => setMessage(null), 3000);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold text-gray-900">Quick Actions</h3>
        {message && (
          <span className={`text-sm px-3 py-1 rounded-full ${
            message.type === 'success' 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {message.text}
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-2">
        {interactionTypes.map(({ type, label, icon: Icon, color }) => (
          <button
            key={type}
            onClick={() => handleInteraction(type)}
            disabled={creating}
            className={`${color} px-4 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            <Icon className="h-4 w-4" />
            <span className="text-sm">{label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default InteractionSimulator;