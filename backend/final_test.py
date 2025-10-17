"""
Final integration test before demo.
Tests all critical paths to ensure everything works.
"""

import requests
import sys
from rich.console import Console
from rich.table import Table

console = Console()
BASE_URL = "http://localhost:8000/api/v1"

def test_backend_health():
    """Test if backend is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            console.print("✅ Backend is running", style="bold green")
            return True
        else:
            console.print("❌ Backend returned non-200 status", style="bold red")
            return False
    except requests.exceptions.ConnectionError:
        console.print("❌ Cannot connect to backend. Is it running?", style="bold red")
        return False

def test_products_endpoint():
    """Test products API."""
    try:
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            console.print(f"✅ Products endpoint works ({len(products)} products)", style="bold green")
            return True, len(products)
        else:
            console.print("❌ Products endpoint failed", style="bold red")
            return False, 0
    except Exception as e:
        console.print(f"❌ Products test failed: {e}", style="bold red")
        return False, 0

def test_users_endpoint():
    """Test users API."""
    try:
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            users = response.json()
            console.print(f"✅ Users endpoint works ({len(users)} users)", style="bold green")
            return True, users[0] if users else None
        else:
            console.print("❌ Users endpoint failed", style="bold red")
            return False, None
    except Exception as e:
        console.print(f"❌ Users test failed: {e}", style="bold red")
        return False, None

def test_recommendations(user_id):
    """Test recommendation generation."""
    try:
        payload = {
            "user_id": user_id,
            "limit": 5,
            "include_explanation": True
        }
        response = requests.post(f"{BASE_URL}/recommendations/generate", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            recs = data.get('recommendations', [])
            
            # Check if explanations exist
            has_explanations = all(rec.get('explanation') for rec in recs)
            
            console.print(f"✅ Recommendations generated ({len(recs)} items)", style="bold green")
            
            if has_explanations:
                console.print("✅ All recommendations have LLM explanations", style="bold green")
            else:
                console.print("⚠️  Some recommendations missing explanations", style="bold yellow")
            
            return True, recs
        else:
            console.print(f"❌ Recommendations failed: {response.status_code}", style="bold red")
            return False, []
    except Exception as e:
        console.print(f"❌ Recommendations test failed: {e}", style="bold red")
        return False, []

def test_interaction_creation(user_id, product_id):
    """Test creating an interaction."""
    try:
        payload = {
            "user_id": user_id,
            "product_id": product_id,
            "interaction_type": "view",
            "duration": 30
        }
        response = requests.post(f"{BASE_URL}/interactions/", json=payload)
        
        if response.status_code == 201:
            console.print("✅ Interaction creation works", style="bold green")
            return True
        else:
            console.print("❌ Interaction creation failed", style="bold red")
            return False
    except Exception as e:
        console.print(f"❌ Interaction test failed: {e}", style="bold red")
        return False

def test_user_insights(user_id):
    """Test user insights endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/recommendations/insights/{user_id}")
        
        if response.status_code == 200:
            data = response.json()
            insights = data.get('insights', {})
            console.print(f"✅ User insights work (Total interactions: {insights.get('total_interactions', 0)})", style="bold green")
            return True
        else:
            console.print("❌ User insights failed", style="bold red")
            return False
    except Exception as e:
        console.print(f"❌ Insights test failed: {e}", style="bold red")
        return False

def display_sample_recommendation(recs):
    """Display a sample recommendation in a nice table."""
    if not recs:
        return
    
    console.print("\n📊 Sample Recommendation:", style="bold cyan")
    
    rec = recs[0]
    product = rec.get('product', {})
    
    table = Table(show_header=False, box=None)
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Product", product.get('name', 'N/A'))
    table.add_row("Category", product.get('category', 'N/A'))
    table.add_row("Price", f"${product.get('price', 0):.2f}")
    table.add_row("Score", f"{rec.get('score', 0):.4f}")
    table.add_row("Rank", str(rec.get('rank', 'N/A')))
    
    console.print(table)
    
    explanation = rec.get('explanation', 'No explanation')
    console.print(f"\n💬 Explanation:", style="bold cyan")
    console.print(f"   {explanation}\n", style="italic")

def main():
    """Run all tests."""
    console.print("\n" + "="*60, style="bold blue")
    console.print("🧪 FINAL INTEGRATION TEST", style="bold blue")
    console.print("="*60 + "\n", style="bold blue")
    
    results = []
    
    # Test 1: Backend health
    console.print("1️⃣  Testing backend health...", style="bold")
    results.append(test_backend_health())
    console.print()
    
    if not results[-1]:
        console.print("❌ Backend not running. Please start it first:", style="bold red")
        console.print("   cd backend && python -m uvicorn app.main:app --reload\n")
        sys.exit(1)
    
    # Test 2: Products
    console.print("2️⃣  Testing products endpoint...", style="bold")
    success, product_count = test_products_endpoint()
    results.append(success)
    console.print()
    
    # Test 3: Users
    console.print("3️⃣  Testing users endpoint...", style="bold")
    success, first_user = test_users_endpoint()
    results.append(success)
    console.print()
    
    if not first_user:
        console.print("❌ No users found. Please run seed_database.py\n", style="bold red")
        sys.exit(1)
    
    user_id = first_user['id']
    
    # Test 4: User insights
    console.print("4️⃣  Testing user insights...", style="bold")
    results.append(test_user_insights(user_id))
    console.print()
    
    # Test 5: Recommendations
    console.print("5️⃣  Testing recommendation generation...", style="bold")
    success, recs = test_recommendations(user_id)
    results.append(success)
    console.print()
    
    # Display sample recommendation
    if recs:
        display_sample_recommendation(recs)
    
    # Test 6: Interactions
    console.print("6️⃣  Testing interaction creation...", style="bold")
    if recs:
        product_id = recs[0]['product_id']
        results.append(test_interaction_creation(user_id, product_id))
    else:
        console.print("⚠️  Skipping (no products to test with)", style="bold yellow")
        results.append(True)
    console.print()
    
    # Summary
    console.print("="*60, style="bold blue")
    total_tests = len(results)
    passed_tests = sum(results)
    
    if passed_tests == total_tests:
        console.print(f"✅ ALL TESTS PASSED ({passed_tests}/{total_tests})", style="bold green")
        console.print("\n🎉 System is ready for demo!", style="bold green")
    else:
        console.print(f"⚠️  {passed_tests}/{total_tests} tests passed", style="bold yellow")
        console.print("\n⚠️  Please fix failing tests before demo", style="bold yellow")
    
    console.print("="*60 + "\n", style="bold blue")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n❌ Tests interrupted by user\n", style="bold red")
        sys.exit(1)