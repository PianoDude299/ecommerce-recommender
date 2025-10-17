"""Quick script to test API endpoints programmatically."""

import requests
import json

BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"


def test_api():
    """Test all major API endpoints."""
    
    print("\n" + "="*70)
    print("🧪 TESTING API ENDPOINTS")
    print("="*70 + "\n")
    
    # Test 1: Root endpoint
    print("1️⃣  Testing root endpoint...")
    response = requests.get(BASE_URL)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
    
    # Test 2: Get products
    print("2️⃣  Testing GET /products...")
    response = requests.get(f"{API_V1}/products/")
    print(f"   Status: {response.status_code}")
    print(f"   Products count: {len(response.json())}\n")
    
    # Test 3: Get users
    print("3️⃣  Testing GET /users...")
    response = requests.get(f"{API_V1}/users/")
    print(f"   Status: {response.status_code}")
    users = response.json()
    print(f"   Users count: {len(users)}")
    if users:
        print(f"   First user: {users[0]['name']} (ID: {users[0]['id']})\n")
    
    # Test 4: Get user insights
    if users:
        user_id = users[0]['id']
        print(f"4️⃣  Testing GET /recommendations/insights/{user_id}...")
        response = requests.get(f"{API_V1}/recommendations/insights/{user_id}")
        print(f"   Status: {response.status_code}")
        insights = response.json()
        print(f"   Total interactions: {insights['insights']['total_interactions']}")
        print(f"   Favorite categories: {[c['category'] for c in insights['insights']['favorite_categories']]}\n")
    
    # Test 5: Generate recommendations
    if users:
        user_id = users[0]['id']
        print(f"5️⃣  Testing POST /recommendations/generate for user {user_id}...")
        payload = {
            "user_id": user_id,
            "limit": 3,
            "include_explanation": True
        }
        response = requests.post(f"{API_V1}/recommendations/generate", json=payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            recommendations = response.json()
            print(f"   Generated {recommendations['total_count']} recommendations:\n")
            
            for rec in recommendations['recommendations']:
                product = rec['product']
                print(f"   • {product['name']}")
                print(f"     Score: {rec['score']:.4f} | Rank: {rec['rank']}")
                print(f"     Explanation: {rec['explanation'][:100]}...")
                print()
    
    print("="*70)
    print("✅ API testing completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API.")
        print("   Make sure the FastAPI server is running on http://localhost:8000")
        print("   Run: python -m uvicorn app.main:app --reload\n")
    except Exception as e:
        print(f"\n❌ Error during API testing: {e}\n")