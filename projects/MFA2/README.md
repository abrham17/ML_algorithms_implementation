# Merchant Financial Agent (MFA)

MFA is a context-aware AI solution designed for **Elodi Tech Security & Electronics Trading PLC**. It consists of a Django backend (serving as the Model Context Protocol layer) and a Flutter mobile application.

## Prerequisites
- **Python 3.10+**
- **Flutter SDK** (Install via `sudo snap install flutter --classic` on Linux)
- **Git**

---

## 1. Backend Setup (Django)

The backend handles the database, authentication, and AI Agent logic (MCP).

### Installation
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install django djangorestframework psycopg2-binary google-generativeai
   ```

### Configuration
1. **Migrations**: Apply database migrations to set up the SQLite DB (default):
   ```bash
   python manage.py migrate
   ```
2. **Environment Variables**:
   - To use the real Gemini AI features, set your API key:
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     ```
   - *Note: Without this, the system uses mock responses or throws errors for chat.*

### Running the Server
Start the development server:
```bash
python manage.py runserver 0.0.0.0:8000
```
The API will be available at `http://localhost:8000/api/`.

### Running Tests
To verify the system integrity:
```bash
python manage.py test api
```

---

## 2. Mobile Setup (Flutter)

The mobile app provides the user interface for Transactions, Chat, and Reporting.

### Installation
1. Navigate to the mobile directory:
   ```bash
   cd mobile
   ```
2. **Initialize Project** (First time only):
   Since the source code (`lib/`) was generated before the Flutter SDK was ready, you must initialize the build files:
   ```bash
   flutter create . --org com.eloditech.mfa --project-name mfa_mobile
   ```
3. Install dependencies:
   ```bash
   flutter pub get
   ```

### Configuration
- **API URL**:
  - The app is pre-configured to connect to `http://10.0.2.2:8000/api` (Android Emulator's alias for localhost).
  - If running on a physical device, update `lib/core/api_service.dart` with your machine's local IP address.

### Running the App
Launch the app on a connected device or emulator:
```bash
flutter run
```

---

## Features
- **Role-Based Access**: Owner vs Staff (Models implemented).
- **Natural Language Chat**: "Sold 5 laptops..." (Powered by Gemini).
- **Manual Transactions**: Form-based entry for Sales/Purchases.
- **Inventory Management**: Automatic stock deduction.
- **Calendar & Market Data**: APIs ready for scheduling and forex rates.
