"""
Sample data generator for e-commerce recommender system.
Creates realistic products, users, and interactions.
"""

from typing import List, Dict, Any
import random
from datetime import datetime, timedelta


class SampleDataGenerator:
    """Generate realistic sample data for the e-commerce system."""
    
    # Product data by category
    PRODUCTS = {
        "Electronics": [
            {
                "name": "Sony WH-1000XM5 Wireless Headphones",
                "description": "Industry-leading noise canceling with premium sound quality. 30-hour battery life and multipoint connection.",
                "price": 399.99,
                "brand": "Sony",
                "attributes": {"color": "Black", "wireless": True, "noise_canceling": True, "battery_life": "30 hours"},
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&h=400&fit=crop"
            },
            {
                "name": "Apple AirPods Pro (2nd Gen)",
                "description": "Active Noise Cancellation and Adaptive Transparency. Personalized Spatial Audio with dynamic head tracking.",
                "price": 249.99,
                "brand": "Apple",
                "attributes": {"color": "White", "wireless": True, "noise_canceling": True, "battery_life": "6 hours"},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1606841837239-c5a1a4a07af7?w=400&h=400&fit=crop"
            },
            {
                "name": "Samsung Galaxy S24 Ultra",
                "description": "Ultimate flagship smartphone with S Pen, 200MP camera, and AI-powered features.",
                "price": 1299.99,
                "brand": "Samsung",
                "attributes": {"color": "Titanium Gray", "storage": "256GB", "screen_size": "6.8 inches", "5g": True},
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&h=400&fit=crop"
            },
            {
                "name": "Apple iPhone 15 Pro",
                "description": "Titanium design with A17 Pro chip. Pro camera system with 5x telephoto.",
                "price": 999.99,
                "brand": "Apple",
                "attributes": {"color": "Natural Titanium", "storage": "256GB", "screen_size": "6.1 inches", "5g": True},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1592286927505-2fd27c0539c2?w=400&h=400&fit=crop"
            },
            {
                "name": "Dell XPS 15 Laptop",
                "description": "15.6-inch 4K OLED display, Intel i7-13700H, 32GB RAM, 1TB SSD. Perfect for creators.",
                "price": 2199.99,
                "brand": "Dell",
                "attributes": {"color": "Platinum Silver", "ram": "32GB", "storage": "1TB SSD", "screen_size": "15.6 inches"},
                "rating": 4.5,
                "image_url": "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&h=400&fit=crop"
            },
            {
                "name": "MacBook Air M3",
                "description": "Supercharged by M3 chip. Up to 18 hours of battery life. Liquid Retina display.",
                "price": 1299.99,
                "brand": "Apple",
                "attributes": {"color": "Midnight", "ram": "16GB", "storage": "512GB SSD", "screen_size": "13.6 inches"},
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=400&fit=crop"
            },
            {
                "name": "LG 27-inch 4K Monitor",
                "description": "27-inch UHD 4K display with HDR10. USB-C connectivity and ergonomic stand.",
                "price": 449.99,
                "brand": "LG",
                "attributes": {"screen_size": "27 inches", "resolution": "4K", "hdr": True, "refresh_rate": "60Hz"},
                "rating": 4.4,
                "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=400&fit=crop"
            },
            {
                "name": "Logitech MX Master 3S Mouse",
                "description": "Wireless performance mouse with ultra-precise scrolling and ergonomic design.",
                "price": 99.99,
                "brand": "Logitech",
                "attributes": {"color": "Graphite", "wireless": True, "dpi": "8000", "buttons": 7},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=400&h=400&fit=crop"
            }
        ],
        "Fashion": [
            {
                "name": "Levi's 501 Original Jeans",
                "description": "The original jean since 1873. Classic straight fit with button fly.",
                "price": 89.99,
                "brand": "Levi's",
                "attributes": {"color": "Dark Wash", "size": "32x32", "fit": "Straight", "material": "100% Cotton"},
                "rating": 4.5,
                "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop"
            },
            {
                "name": "Nike Air Max 270",
                "description": "Lifestyle sneakers with large Max Air unit. Breathable mesh upper.",
                "price": 150.00,
                "brand": "Nike",
                "attributes": {"color": "Triple Black", "size": "10", "type": "Sneakers", "cushioning": "Air Max"},
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"
            },
            {
                "name": "Adidas Ultraboost 23",
                "description": "Running shoes with responsive Boost cushioning. Primeknit upper for comfort.",
                "price": 190.00,
                "brand": "Adidas",
                "attributes": {"color": "Core Black", "size": "10.5", "type": "Running", "cushioning": "Boost"},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&h=400&fit=crop"
            },
            {
                "name": "Ray-Ban Aviator Classic",
                "description": "Iconic teardrop-shaped sunglasses with metal frame. 100% UV protection.",
                "price": 179.99,
                "brand": "Ray-Ban",
                "attributes": {"color": "Gold/Green", "frame_material": "Metal", "lens_type": "Polarized", "uv_protection": True},
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=400&h=400&fit=crop"
            },
            {
                "name": "The North Face Nuptse Jacket",
                "description": "Iconic insulated jacket with 700-fill down. Water-repellent finish.",
                "price": 329.99,
                "brand": "The North Face",
                "attributes": {"color": "Black", "size": "M", "insulation": "700-fill Down", "water_resistant": True},
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=400&fit=crop"
            },
            {
                "name": "Patagonia Better Sweater",
                "description": "Classic fleece jacket made with recycled polyester. Quarter-zip design.",
                "price": 139.99,
                "brand": "Patagonia",
                "attributes": {"color": "Navy Blue", "size": "L", "material": "Recycled Polyester", "style": "Quarter-Zip"},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=400&fit=crop"
            }
        ],
        "Home & Kitchen": [
            {
                "name": "KitchenAid Stand Mixer",
                "description": "5-quart tilt-head stand mixer with 10 speeds. Includes multiple attachments.",
                "price": 449.99,
                "brand": "KitchenAid",
                "attributes": {"color": "Empire Red", "capacity": "5 quart", "speeds": 10, "attachments": 3},
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=400&fit=crop"
            },
            {
                "name": "Ninja Professional Blender",
                "description": "1000-watt motor with Total Crushing Technology. 72 oz pitcher.",
                "price": 99.99,
                "brand": "Ninja",
                "attributes": {"color": "Black", "capacity": "72 oz", "power": "1000W", "blades": "6-blade"},
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop"
            },
            {
                "name": "Instant Pot Duo Plus",
                "description": "9-in-1 electric pressure cooker. 6-quart capacity with smart programs.",
                "price": 119.99,
                "brand": "Instant Pot",
                "attributes": {"color": "Stainless Steel", "capacity": "6 quart", "programs": 9, "pressure_cook": True},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop"
            },
            {
                "name": "Dyson V15 Detect Vacuum",
                "description": "Cordless vacuum with laser detection. 60-minute runtime and LCD screen.",
                "price": 749.99,
                "brand": "Dyson",
                "attributes": {"color": "Yellow/Nickel", "cordless": True, "runtime": "60 min", "laser_detect": True},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=400&h=400&fit=crop"
            },
            {
                "name": "Cuisinart Coffee Maker",
                "description": "12-cup programmable coffee maker with brew strength control. Self-cleaning.",
                "price": 89.99,
                "brand": "Cuisinart",
                "attributes": {"color": "Stainless Steel", "capacity": "12 cup", "programmable": True, "brew_strength": True},
                "rating": 4.5,
                "image_url": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=400&fit=crop"
            }
        ],
        "Books": [
            {
                "name": "Atomic Habits by James Clear",
                "description": "Proven framework for improving every day. Tiny changes, remarkable results.",
                "price": 16.99,
                "brand": "Avery",
                "attributes": {"author": "James Clear", "pages": 320, "format": "Hardcover", "genre": "Self-Help"},
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=400&fit=crop"
            },
            {
                "name": "The Psychology of Money",
                "description": "Timeless lessons on wealth, greed, and happiness by Morgan Housel.",
                "price": 18.99,
                "brand": "Harriman House",
                "attributes": {"author": "Morgan Housel", "pages": 256, "format": "Paperback", "genre": "Finance"},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=400&h=400&fit=crop"
            },
            {
                "name": "Project Hail Mary by Andy Weir",
                "description": "A lone astronaut must save the earth in this interstellar thriller.",
                "price": 19.99,
                "brand": "Ballantine Books",
                "attributes": {"author": "Andy Weir", "pages": 496, "format": "Hardcover", "genre": "Science Fiction"},
                "rating": 4.9,
                "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&h=400&fit=crop"
            },
            {
                "name": "Thinking, Fast and Slow",
                "description": "Explores the two systems that drive the way we think by Daniel Kahneman.",
                "price": 17.99,
                "brand": "Farrar, Straus and Giroux",
                "attributes": {"author": "Daniel Kahneman", "pages": 499, "format": "Paperback", "genre": "Psychology"},
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400&h=400&fit=crop"
            }
        ],
        "Sports & Outdoors": [
            {
                "name": "YETI Rambler 30 oz Tumbler",
                "description": "Stainless steel insulated tumbler. Keeps drinks cold for 24 hours, hot for 6 hours.",
                "price": 39.99,
                "brand": "YETI",
                "attributes": {"color": "Navy", "capacity": "30 oz", "insulated": True, "dishwasher_safe": True},
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=400&fit=crop"
            },
            {
                "name": "Hydro Flask Water Bottle",
                "description": "32 oz insulated water bottle. TempShield technology keeps beverages cold for 24 hours.",
                "price": 44.95,
                "brand": "Hydro Flask",
                "attributes": {"color": "Pacific", "capacity": "32 oz", "insulated": True, "bpa_free": True},
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=400&h=400&fit=crop"
            },
            {
                "name": "Black Diamond Headlamp",
                "description": "Rechargeable LED headlamp with 500 lumens. Waterproof and adjustable beam.",
                "price": 49.95,
                "brand": "Black Diamond",
                "attributes": {"color": "Black", "lumens": 500, "rechargeable": True, "waterproof": True},
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1504805572947-34fad45aed93?w=400&h=400&fit=crop"
            },
            {
                "name": "Manduka Pro Yoga Mat",
                "description": "Professional-grade yoga mat with lifetime guarantee. 6mm thick, superior cushioning.",
                "price": 138.00,
                "brand": "Manduka",
                "attributes": {"color": "Black", "thickness": "6mm", "material": "PVC", "length": "71 inches"},
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=400&fit=crop"
            }
        ]
    }
    
    # User personas
    USERS = [
        {
            "name": "Alex Chen",
            "email": "alex.chen@email.com",
            "preferences": {
                "budget": "high",
                "interests": ["electronics", "tech", "productivity"],
                "favorite_brands": ["Apple", "Sony", "Dell"]
            }
        },
        {
            "name": "Sarah Johnson",
            "email": "sarah.j@email.com",
            "preferences": {
                "budget": "medium",
                "interests": ["fashion", "lifestyle", "wellness"],
                "favorite_brands": ["Nike", "Levi's", "Patagonia"]
            }
        },
        {
            "name": "Michael Park",
            "email": "m.park@email.com",
            "preferences": {
                "budget": "high",
                "interests": ["home", "cooking", "quality"],
                "favorite_brands": ["KitchenAid", "Dyson", "YETI"]
            }
        },
        {
            "name": "Emma Davis",
            "email": "emma.davis@email.com",
            "preferences": {
                "budget": "low",
                "interests": ["books", "learning", "self-improvement"],
                "favorite_brands": ["Avery", "Penguin Random House"]
            }
        },
        {
            "name": "James Wilson",
            "email": "james.w@email.com",
            "preferences": {
                "budget": "medium",
                "interests": ["sports", "outdoors", "fitness"],
                "favorite_brands": ["YETI", "Black Diamond", "Manduka"]
            }
        },
        {
            "name": "Olivia Martinez",
            "email": "olivia.m@email.com",
            "preferences": {
                "budget": "high",
                "interests": ["fashion", "tech", "premium"],
                "favorite_brands": ["Apple", "Ray-Ban", "The North Face"]
            }
        },
        {
            "name": "David Lee",
            "email": "david.lee@email.com",
            "preferences": {
                "budget": "medium",
                "interests": ["tech", "gaming", "productivity"],
                "favorite_brands": ["Samsung", "LG", "Logitech"]
            }
        },
        {
            "name": "Sophie Turner",
            "email": "sophie.t@email.com",
            "preferences": {
                "budget": "low",
                "interests": ["home", "cooking", "budget-friendly"],
                "favorite_brands": ["Ninja", "Cuisinart", "Instant Pot"]
            }
        }
    ]
    
    @classmethod
    def generate_products(cls) -> List[Dict[str, Any]]:
        """Generate all products with categories."""
        all_products = []
        for category, products in cls.PRODUCTS.items():
            for product in products:
                product_data = product.copy()
                product_data["category"] = category
                product_data["stock"] = random.randint(50, 500)
                all_products.append(product_data)
        return all_products
    
    @classmethod
    def generate_users(cls) -> List[Dict[str, Any]]:
        """Generate all users."""
        return cls.USERS.copy()
    
    @classmethod
    def generate_interactions(
        cls,
        user_ids: List[int],
        product_ids: List[int],
        num_interactions: int = 200
    ) -> List[Dict[str, Any]]:
        """Generate realistic user interactions."""
        interactions = []
        interaction_types = ["view", "click", "cart", "purchase", "rating"]
        type_weights = [0.5, 0.25, 0.15, 0.08, 0.02]  # Views are most common
        
        for _ in range(num_interactions):
            user_id = random.choice(user_ids)
            product_id = random.choice(product_ids)
            interaction_type = random.choices(interaction_types, weights=type_weights)[0]
            
            # Generate realistic timestamps (last 30 days)
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            timestamp = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
            
            interaction = {
                "user_id": user_id,
                "product_id": product_id,
                "interaction_type": interaction_type,
                "timestamp": timestamp
            }
            
            # Add duration for views
            if interaction_type == "view":
                interaction["duration"] = random.randint(5, 300)  # 5 seconds to 5 minutes
            
            # Add rating for rating interactions
            if interaction_type == "rating":
                interaction["rating"] = round(random.uniform(3.0, 5.0), 1)
            
            # Add context
            if interaction_type in ["view", "click"]:
                sources = ["search", "recommendation", "category_browse", "direct"]
                interaction["context"] = {"source": random.choice(sources)}
            
            interactions.append(interaction)
        
        # Sort by timestamp
        interactions.sort(key=lambda x: x["timestamp"])
        
        return interactions