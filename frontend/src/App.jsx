import React, { useState, useEffect } from 'react';
import { Sparkles, ShoppingBag, RefreshCw, TrendingUp, Zap } from 'lucide-react';
import UserSelector from './components/UserSelector';
import UserInsights from './components/UserInsights';
import RecommendationCard from './components/RecommendationCard';
import ProductCard from './components/ProductCard';
import ProductModal from './components/ProductModal';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { recommendationsApi, productsApi } from './services/api';

function App() {
  const [selectedUser, setSelectedUser] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [showProductModal, setShowProductModal] = useState(false);
  const [activeTab, setActiveTab] = useState('recommendations'); // recommendations, products

  useEffect(() => {
    fetchProducts();
  }, []);

  useEffect(() => {
    if (selectedUser) {
      fetchRecommendations();
    }
  }, [selectedUser]);

  const fetchProducts = async () => {
    try {
      const response = await productsApi.getAll();
      setProducts(response.data);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    }
  };

  const fetchRecommendations = async () => {
    if (!selectedUser) return;

    setLoading(true);
    setError(null);

    try {
      const response = await recommendationsApi.generate({
        user_id: selectedUser.id,
        limit: 6,
        include_explanation: true,
      });

      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
      setError('Failed to load recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleProductView = (product) => {
    setSelectedProduct(product);
    setShowProductModal(true);
  };

  const handleInteractionCreated = () => {
    // Refresh recommendations after interaction
    if (selectedUser) {
      fetchRecommendations();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-3 rounded-xl shadow-lg">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  AI Product Recommender
                </h1>
                <p className="text-sm text-gray-600">
                  Personalized recommendations powered by machine learning
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-4 gap-8">
          {/* Left Sidebar - User Selection & Insights */}
          <div className="lg:col-span-1 space-y-6">
            {/* User Selector */}
            <div className="card p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Select User
              </h2>
              <UserSelector
                selectedUser={selectedUser}
                onUserSelect={setSelectedUser}
              />
            </div>

            {/* User Insights */}
            {selectedUser && (
              <div className="card p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">
                    User Insights
                  </h2>
                  <TrendingUp className="h-5 w-5 text-primary-600" />
                </div>
                <UserInsights userId={selectedUser.id} />
              </div>
            )}
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3 space-y-6">
            {/* Action Bar */}
            {selectedUser && (
              <div className="card p-4">
                <div className="flex items-center justify-between">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => setActiveTab('recommendations')}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2 ${
                        activeTab === 'recommendations'
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <Zap className="h-4 w-4" />
                      <span>Recommendations</span>
                    </button>
                    <button
                      onClick={() => setActiveTab('products')}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2 ${
                        activeTab === 'products'
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <ShoppingBag className="h-4 w-4" />
                      <span>All Products</span>
                    </button>
                  </div>

                  {activeTab === 'recommendations' && (
                    <button
                      onClick={fetchRecommendations}
                      disabled={loading}
                      className="btn-primary flex items-center space-x-2 disabled:opacity-50"
                    >
                      <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                      <span>Refresh</span>
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Content */}
            {!selectedUser ? (
              <div className="card p-12 text-center">
                <Sparkles className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Get Started
                </h3>
                <p className="text-gray-600">
                  Select a user from the sidebar to see personalized recommendations
                </p>
              </div>
            ) : activeTab === 'recommendations' ? (
              <>
                {loading ? (
                  <LoadingSpinner text="Generating personalized recommendations..." />
                ) : error ? (
                  <ErrorMessage message={error} onRetry={fetchRecommendations} />
                ) : recommendations.length > 0 ? (
                  <>
                    <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-xl p-6 border border-primary-100">
                      <div className="flex items-start space-x-3">
                        <Sparkles className="h-6 w-6 text-primary-600 flex-shrink-0" />
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900 mb-1">
                            Personalized for {selectedUser.name}
                          </h3>
                          <p className="text-gray-700">
                            Based on {selectedUser.name.split(' ')[0]}'s browsing history, 
                            preferences, and similar users' choices
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {recommendations.map((rec) => (
                        <RecommendationCard
                          key={rec.product_id}
                          recommendation={rec}
                          onView={() => handleProductView(rec.product)}
                          showExplanation={true}
                        />
                      ))}
                    </div>
                  </>
                ) : (
                  <div className="card p-12 text-center">
                    <ShoppingBag className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      No Recommendations Yet
                    </h3>
                    <p className="text-gray-600 mb-4">
                      Start interacting with products to get personalized recommendations
                    </p>
                    <button
                      onClick={() => setActiveTab('products')}
                      className="btn-primary"
                    >
                      Browse Products
                    </button>
                  </div>
                )}
              </>
            ) : (
              <>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-gray-900">
                    All Products ({products.length})
                  </h3>
                </div>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {products.map((product) => (
                    <ProductCard
                      key={product.id}
                      product={product}
                      onView={() => handleProductView(product)}
                    />
                  ))}
                </div>
              </>
            )}
          </div>
        </div>
      </main>

      {/* Product Modal */}
      <ProductModal
        product={selectedProduct}
        userId={selectedUser?.id}
        isOpen={showProductModal}
        onClose={() => setShowProductModal(false)}
        onInteractionCreated={handleInteractionCreated}
      />

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            AI-Powered E-commerce Recommender • Built with React, FastAPI & Google Gemini
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;