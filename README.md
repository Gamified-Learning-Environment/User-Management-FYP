# Gamified Learning Environment (GLE) - User Management Microservice
Welcome to the User Management Microservice Repository for the Gamified Learning Environment (GLE) project! This microservice handles all user-related operations including authentication, profile management, and user data persistence.

## Service Overview
This microservice is part of a larger ecosystem designed to create an engaging online learning environment. It provides the fundamental user management capabilities that support the platform's personalized learning experience and gamification features.

## Features
### Core Authentication Features
1. User Authentication:
  - Secure login and registration system
  - Session management and persistence
  - Token-based authentication for microservice communication


2. Profile Management:
  - User profile creation and updates
  - Role-based access control (student/educator)
  - Account settings management


3. Data Management:

  - Secure storage of user credentials
  - Profile data persistence
  - Integration with gamification tracking

## Technologies Used
### Backend Framework
- Flask: Python-based RESTful API development
- MongoDB: Document-based storage for user data
  - Utilizing JSON format
  - Key-value pair storage for efficient data retrieval


## API Endpoints
The service exposes RESTful endpoints for:
- User registration
- Authentication
- Profile management
- Session handling

## System Architecture
### Microservice Integration
This service is one of four independent microservices in the GLE platform:
- User Management (This service)
- Quiz Generation
- Results Tracking
- Gamification
