# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Currently no authentication required (add for production).

---

## Products API

### List Products
```http
GET /api/v1/products/
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum records to return (default: 100)
- `category` (string, optional): Filter by category

**Response:**
```json
[
  {
    "id": 1,
    "name": "Sony WH-1000XM5 Wireless Headphones",
    "description": "Industry-leading noise canceling...",
    "category": "Electronics",
    "price": 399.99,
    "brand": "Sony",
    "attributes": {...},
    "image_url": "https://...",
    "stock": 150,
    "rating": 4.8,
    "created_at": "2025-10-17T00:00:00"
  }
]
```

### Get Product by ID
```http
GET /api/v1/products/{product_id}
```

### Get Categories
```http
GET /api/v1/products/categories/list
```

**Response:**
```json
{
  "categories": ["Electronics", "Fashion", "Home & Kitchen", "Books", "Sports & Outdoors"]
}
```

---

## Users API

### List Users
```http
GET /api/v1/users/
```

### Get User by ID
```http
GET /api/v1/users/{user_id}
```

### Create User
```http
POST /api/v1/users/
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "preferences": {
    "budget": "medium",
    "interests": ["electronics", "books"]
  }
}
```

---

## Interactions API

### Create Interaction
```http
POST /api/v1/interactions/
```

**Request Body:**
```json
{
  "user_id": 1,
  "product_id": 5,
  "interaction_type": "purchase",
  "duration": 120,
  "rating": 4.5,
  "context": {"source": "recommendation"}
}
```

**Interaction Types:**
- `view` - User viewed product
- `click` - User clicked product
- `cart` - User added to cart
- `purchase` - User purchased product
- `rating` - User rated product

---

## Recommendations API

### Generate Recommendations
```http
POST /api/v1/recommendations/generate
```

**Request Body:**
```json
{
  "user_id": 1,
  "limit": 10,
  "include_explanation": true
}
```

**Response:**
```json
{
  "user_id": 1,
  "recommendations": [
    {
      "id": 1,
      "product_id": 5,
      "product": {...},
      "score": 0.8542,
      "algorithm_used": "hybrid",
      "explanation": "Based on your recent interest in...",
      "rank": 1,
      "created_at": "2025-10-17T12:00:00"
    }
  ],
  "total_count": 10,
  "generated_at": "2025-10-17T12:00:00"
}
```

### Get User Insights
```http
GET /api/v1/recommendations/insights/{user_id}
```

**Response:**
```json
{
  "user_id": 1,
  "user_name": "Alex Chen",
  "insights": {
    "total_interactions": 45,
    "favorite_categories": [
      {"category": "Electronics", "count": 28}
    ],
    "favorite_brands": [
      {"brand": "Apple", "count": 15}
    ],
    "avg_price": 450.50,
    "recent_purchases": [...]
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```