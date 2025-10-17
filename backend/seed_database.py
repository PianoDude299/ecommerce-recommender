"""
Database seeding script for e-commerce recommender system.
Populates the database with sample products, users, and interactions.
"""

from app.database import init_db, drop_db, get_db
from app.models.database import Product, User, Interaction
from data.sample_data import SampleDataGenerator
from sqlalchemy.orm import Session


def seed_products(db: Session) -> list[int]:
    """Seed products into database."""
    print("📦 Seeding products...")
    
    products_data = SampleDataGenerator.generate_products()
    product_ids = []
    
    for product_data in products_data:
        product = Product(**product_data)
        db.add(product)
        db.flush()  # Get the ID without committing
        product_ids.append(product.id)
    
    db.commit()
    print(f"   ✅ Added {len(product_ids)} products")
    return product_ids


def seed_users(db: Session) -> list[int]:
    """Seed users into database."""
    print("👥 Seeding users...")
    
    users_data = SampleDataGenerator.generate_users()
    user_ids = []
    
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        db.flush()
        user_ids.append(user.id)
    
    db.commit()
    print(f"   ✅ Added {len(user_ids)} users")
    return user_ids


def seed_interactions(db: Session, user_ids: list[int], product_ids: list[int]) -> None:
    """Seed interactions into database."""
    print("🔄 Seeding interactions...")
    
    interactions_data = SampleDataGenerator.generate_interactions(
        user_ids=user_ids,
        product_ids=product_ids,
        num_interactions=300  # Generate 300 interactions
    )
    
    for interaction_data in interactions_data:
        interaction = Interaction(**interaction_data)
        db.add(interaction)
    
    db.commit()
    print(f"   ✅ Added {len(interactions_data)} interactions")


def print_database_summary(db: Session) -> None:
    """Print summary of database contents."""
    print("\n" + "="*60)
    print("📊 DATABASE SUMMARY")
    print("="*60)
    
    # Count records
    product_count = db.query(Product).count()
    user_count = db.query(User).count()
    interaction_count = db.query(Interaction).count()
    
    print(f"\n📦 Products: {product_count}")
    
    # Products by category
    from sqlalchemy import func
    category_counts = db.query(
        Product.category,
        func.count(Product.id)
    ).group_by(Product.category).all()
    
    for category, count in category_counts:
        print(f"   • {category}: {count}")
    
    print(f"\n👥 Users: {user_count}")
    
    # Sample users
    sample_users = db.query(User).limit(3).all()
    for user in sample_users:
        print(f"   • {user.name} ({user.email})")
    print(f"   • ... and {user_count - 3} more")
    
    print(f"\n🔄 Interactions: {interaction_count}")
    
    # Interactions by type
    interaction_counts = db.query(
        Interaction.interaction_type,
        func.count(Interaction.id)
    ).group_by(Interaction.interaction_type).all()
    
    for int_type, count in interaction_counts:
        percentage = (count / interaction_count) * 100
        print(f"   • {int_type}: {count} ({percentage:.1f}%)")
    
    # Most active user
    most_active = db.query(
        User.name,
        func.count(Interaction.id).label('interaction_count')
    ).join(Interaction).group_by(User.id).order_by(
        func.count(Interaction.id).desc()
    ).first()
    
    if most_active:
        print(f"\n🏆 Most Active User: {most_active[0]} ({most_active[1]} interactions)")
    
    # Most viewed product
    most_viewed = db.query(
        Product.name,
        func.count(Interaction.id).label('view_count')
    ).join(Interaction).filter(
        Interaction.interaction_type == 'view'
    ).group_by(Product.id).order_by(
        func.count(Interaction.id).desc()
    ).first()
    
    if most_viewed:
        print(f"👁️  Most Viewed Product: {most_viewed[0]} ({most_viewed[1]} views)")
    
    print("\n" + "="*60)
    print("✅ Database seeding completed successfully!")
    print("="*60 + "\n")


def main():
    """Main seeding function."""
    print("\n" + "🌱 STARTING DATABASE SEED PROCESS" + "\n")
    print("⚠️  This will drop all existing data and create fresh data.\n")
    
    # Drop and recreate database
    drop_db()
    init_db()
    
    # Get database session
    db = next(get_db())
    
    try:
        # Seed data in order
        product_ids = seed_products(db)
        user_ids = seed_users(db)
        seed_interactions(db, user_ids, product_ids)
        
        # Print summary
        print_database_summary(db)
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()