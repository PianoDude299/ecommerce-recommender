# Testing Checklist

## Pre-Demo Verification

### Backend Tests
- [ ] Backend server starts without errors
- [ ] Can access Swagger docs at http://localhost:8000/docs
- [ ] All API endpoints return expected responses
- [ ] Database has sample data (27+ products, 8 users, 300+ interactions)
- [ ] LLM explanations are being generated successfully
- [ ] No console errors in backend terminal

### Frontend Tests
- [ ] Frontend server starts without errors
- [ ] Application loads at http://localhost:5173
- [ ] No console errors in browser DevTools
- [ ] Images load properly for all products
- [ ] Tailwind CSS styles are applied correctly

### Core Functionality Tests
- [ ] User can be selected from dropdown
- [ ] User insights panel displays correctly
- [ ] Recommendations can be generated
- [ ] LLM explanations appear for each recommendation
- [ ] Product cards display properly
- [ ] Product modal opens when clicking a product
- [ ] Quick actions work (View, Click, Cart, Purchase, Rate)
- [ ] Recommendations refresh after new interaction
- [ ] "All Products" tab shows complete catalog
- [ ] UI is responsive and animations work smoothly

### Data Flow Tests
- [ ] Creating interaction updates the database
- [ ] New interactions affect future recommendations
- [ ] User insights update based on new data
- [ ] Recommendation scores are calculated correctly
- [ ] Diversity filter prevents category dominance

### Edge Cases
- [ ] System handles user with no interactions (shows popular products)
- [ ] System handles rapid clicks without breaking
- [ ] Long product names don't break UI
- [ ] Missing product attributes handled gracefully
- [ ] API errors are caught and displayed properly

### Performance Tests
- [ ] Recommendation generation completes in < 2 seconds
- [ ] LLM explanation generation completes in < 1 second
- [ ] Page loads quickly without lag
- [ ] No memory leaks after extended use
- [ ] Multiple users can be switched smoothly

## Demo Day Checklist

### Before Recording
- [ ] Close unnecessary browser tabs
- [ ] Close unnecessary applications
- [ ] Clear browser cache
- [ ] Test audio recording
- [ ] Test screen recording software
- [ ] Prepare a script/outline
- [ ] Have backup demo data ready
- [ ] Check lighting (if showing webcam)

### Environment Setup
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Browser at http://localhost:5173
- [ ] Browser window properly sized (1920x1080 recommended)
- [ ] Browser DevTools closed
- [ ] Full screen or focused window mode

### Data Preparation
- [ ] Database seeded with fresh data
- [ ] Have specific user personas in mind to demo
- [ ] Know which products to showcase
- [ ] Prepare 2-3 interaction scenarios