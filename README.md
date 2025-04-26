# Gamified Learning Environment (GLE) - User Management Microservice
Welcome to the User Management Microservice Repository for the Gamified Learning Environment (GLE) project! This microservice handles all user-related operations including authentication, profile management, and user data persistence. See the Frontend and the Project Dissertation for greater details.

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

## Deployment and Running
While you could download, compile and run each of the repositories for this Final Year Project and get a more in depth look into the code, it is also fully deployed on Railway at the following link : https://exper-frontend-production.up.railway.app

Alternatively, here's a QR Code: 

![ExperQRCode](https://github.com/user-attachments/assets/57795718-9c35-462c-b257-03cf354f5bd4)

Should this not be sufficient for grading, please see the instructions below: 

### Prerequisites
Node.js (v18+) and npm/yarn
Python (v3.9+)
MongoDB database
API keys for:
OpenAI
Anthropic Claude (optional)
Google Gemini (optional)

### Setup and Installation
1. Clone each repository for this project.
2. For each microservice repeat these steps
      1. 
         ```
         cd service-directory  # e.g., Quiz-Generation-FYP
         python -m venv venv
         source venv/bin/activate  # On Windows: venv\Scripts\activate
         pip install -r requirements.txt
         ```
         
      2. Environmental Variables
         Create a .env file in each microservice directory with appropriate values:
         ```
            MONGODB_URI=mongodb://localhost:27017/quizdb
            OPENAI_API_KEY=your_openai_key
            ANTHROPIC_API_KEY=your_anthropic_key  # Optional
            GOOGLE_API_KEY=your_gemini_key  # Optional
         ```
         User Management Service
         ```
         MONGODB_URI=mongodb://localhost:27017/userdb
         JWT_SECRET=your_jwt_secret
         ```

         Results Tracking Service
         ```
         MONGODB_URI=mongodb://localhost:27017/resultsdb
         ```
         Gamification Service
         ```
         MONGODB_URI=mongodb://localhost:27017/gamificationdb
         ```

3. Frontend Setup
      ```
      cd Exper-Frontend/experfrontend
      npm install
      ```
      Create a .env.local file with:
      ```
      NEXT_PUBLIC_USER_SERVICE_URL=http://localhost:8080
      NEXT_PUBLIC_QUIZ_SERVICE_URL=http://localhost:9090
      NEXT_PUBLIC_RESULTS_SERVICE_URL=http://localhost:8081
      NEXT_PUBLIC_GAMIFICATION_SERVICE_URL=http://localhost:8082
      ```

4. Running the Application
   1. Start the microservices, run each in a seperate terminal:
      ```
      # Quiz Generation Service
      cd Quiz-Generation-FYP
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      python app.py  # Will run on port 9090
      
      # User Management Service
      cd User-Management-Service
      source venv/bin/activate
      python app.py  # Will run on port 8080
      
      # Results Tracking Service
      cd Results-Tracking-FYP
      source venv/bin/activate
      python app.py  # Will run on port 8081
      
      # Gamification Service
      cd Gamification-FYP
      source venv/bin/activate
      python app.py  # Will run on port 8082
      ```
   2. Start the Frontend
      ```
      cd Exper-Frontend/experfrontend
      npm run dev
      ```
   Visit http://localhost:3000 to access the application.
