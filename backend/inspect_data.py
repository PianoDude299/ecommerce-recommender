"""Quick script to inspect database contents."""

from app.database import get_db
from app.models.database import Product, User, Interaction
from sqlalchemy import func


def inspect_database():
    """Inspect and display database contents."""
    db = next(get_db())
    
    try:
        print("\n" + "="*60)
        print("🔍 DATABASE INSPECTION")
        print("="*60 + "\n")
        
        # Show sample products
        print("📦 SAMPLE PRODUCTS:")
        products = db.query(Product).limit(5).all()
        for p in products:
            print(f"\n   {p.name}")
            print(f"   Category: {p.category} | Price: ${p.price} | Rating: {p.rating}⭐")
            print(f"   Brand: {p.brand}")
        
        # Show sample users
        print("\n\n👥 SAMPLE USERS:")
        users = db.query(User).limit(3).all()
        for u in users:
            interaction_count = db.query(Interaction).filter(
                Interaction.user_id == u.id
            ).count()
            print(f"\n   {u.name} ({u.email})")
            print(f"   Interactions: {interaction_count}")
            print(f"   Preferences: {u.preferences}")
        
        # Show recent interactions
        print("\n\n🔄 RECENT INTERACTIONS:")
        recent = db.query(Interaction).order_by(
            Interaction.timestamp.desc()
        ).limit(10).all()
        
        for inter in recent:
            user = db.query(User).filter(User.id == inter.user_id).first()
            product = db.query(Product).filter(Product.id == inter.product_id).first()
            print(f"\n   {user.name} -> {inter.interaction_type.upper()} -> {product.name}")
            print(f"   Time: {inter.timestamp.strftime('%Y-%m-%d %H:%M')}")
        
        print("\n" + "="*60 + "\n")
        
    finally:
        db.close()


if __name__ == "__main__":
    inspect_database()