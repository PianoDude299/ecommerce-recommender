from app.database import init_db, drop_db, get_db
from app.models.database import Product, User, Interaction
from app.config import get_settings

def test_database_setup():
    """Test database initialization and basic operations."""
    
    print("🔧 Testing database setup...")
    
    # Initialize database
    init_db()
    
    # Test creating a product
    db = next(get_db())
    
    try:
        # Create test product
        test_product = Product(
            name="Test Laptop",
            description="A powerful laptop for testing",
            category="Electronics",
            price=999.99,
            brand="TestBrand",
            attributes={"color": "Silver", "ram": "16GB"},
            rating=4.5
        )
        db.add(test_product)
        db.commit()
        db.refresh(test_product)
        
        print(f"✅ Product created: {test_product}")
        
        # Create test user
        test_user = User(
            name="Test User",
            email="test@example.com",
            preferences={"budget": "medium", "interests": ["electronics"]}
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"✅ User created: {test_user}")
        
        # Create test interaction
        test_interaction = Interaction(
            user_id=test_user.id,
            product_id=test_product.id,
            interaction_type="view",
            duration=45,
            context={"source": "search"}
        )
        db.add(test_interaction)
        db.commit()
        db.refresh(test_interaction)
        
        print(f"✅ Interaction created: {test_interaction}")
        
        # Query test
        products = db.query(Product).all()
        users = db.query(User).all()
        interactions = db.query(Interaction).all()
        
        print(f"\n📊 Database Status:")
        print(f"   Products: {len(products)}")
        print(f"   Users: {len(users)}")
        print(f"   Interactions: {len(interactions)}")
        
        print("\n✅ Database setup test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during database test: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Drop existing tables and recreate
    drop_db()
    test_database_setup()