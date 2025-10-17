# System Architecture

## Overview
This document describes the architecture of the AI-Powered E-commerce Recommender system.

## High-Level Architecture

The system follows a three-tier architecture:
1. **Presentation Layer** (React Frontend)
2. **Application Layer** (FastAPI Backend)
3. **Data Layer** (SQLite Database)

## Backend Architecture

### API Layer
- **FastAPI Framework**: Handles HTTP requests/responses
- **Router Pattern**: Organizes endpoints by domain
- **Pydantic Schemas**: Validates request/response data
- **CORS Middleware**: Enables cross-origin requests

### Service Layer
- **RecommendationEngine**: Core algorithm implementation
- **LLMExplanationService**: LLM integration for explanations
- **Database Service**: Data access and persistence

### Data Models
- **Product**: Product catalog information
- **User**: User profiles and preferences
- **Interaction**: User-product interaction history
- **Recommendation**: Generated recommendations with explanations

## Recommendation Algorithm

### Phase 1: Data Collection
```
User Interactions → Database → Interaction Matrix
```

### Phase 2: Collaborative Filtering
```
1. Build user-product matrix with weighted interactions
2. Calculate cosine similarity between users
3. Find K most similar users
4. Aggregate scores from similar users
```

### Phase 3: Content-Based Filtering
```
1. Extract user profile from interaction history
2. Calculate product similarity based on:
   - Category matching
   - Brand preferences
   - Price similarity
   - Attribute matching
```

### Phase 4: Hybrid Fusion
```
hybrid_score = 0.6 * collab_score + 0.4 * content_score
```

### Phase 5: Post-Processing
```
1. Apply diversity filter
2. Sort by score
3. Select top-K recommendations
```

### Phase 6: LLM Explanation
```
1. Build context from user insights
2. Call Gemini API
3. Generate personalized explanation
4. Store with recommendation
```

## Frontend Architecture

### Component Hierarchy
```
App
├── UserSelector
├── UserInsights
├── RecommendationCard[]
│   └── ProductCard
├── ProductModal
│   └── InteractionSimulator
└── ProductCard[]
```

### State Management
- Local component state (useState)
- No global state library needed (small app)
- API calls managed via axios

### Data Flow
```
User Action → Component → API Call → Backend → Database
                ↓
            Update State → Re-render
```

## Database Schema

See `backend/app/models/database.py` for detailed schema definitions.

## Security Considerations

### Current Implementation
- CORS enabled for development
- No authentication (demo purposes)
- Input validation via Pydantic

### Production Recommendations
- Add JWT authentication
- Implement rate limiting
- Use HTTPS only
- Add API key management
- Implement request logging
- Add CSRF protection

## Scalability Considerations

### Current Limitations
- SQLite (single file)
- Synchronous recommendation generation
- No caching layer

### Scaling Recommendations
- Migrate to PostgreSQL/MySQL
- Add Redis for caching
- Implement async recommendation generation
- Add load balancer
- Separate recommendation service
- Use CDN for frontend assets