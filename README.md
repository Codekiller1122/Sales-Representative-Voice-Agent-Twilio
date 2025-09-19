Twilio Django + React Example (Browser-to-Browser and Browser-to-Phone audio calls)
================================================================================

This repository contains a minimal example showing how to:
  - Generate Twilio Access Tokens in Django
  - Expose a TwiML endpoint to control call routing
  - Use a React frontend with Twilio Voice SDK to make/receive audio calls

IMPORTANT
- Fill in your Twilio credentials in environment variables or a .env file.
- Create a TwiML App in Twilio Console and set its Voice URL to:
    https://<your-domain>/api/voice/
  Then use the TwiML App SID as TWIML_APP_SID.

Backend (Django)
----------------
- Requirements: Python 3.10+, pip install -r requirements.txt
- Run:
    export TWILIO_ACCOUNT_SID=...
    export TWILIO_API_KEY_SID=...
    export TWILIO_API_KEY_SECRET=...
    export TWIML_APP_SID=...
    export TWILIO_PHONE_NUMBER=...
    python manage.py migrate
    python manage.py runserver 0.0.0.0:8000

Endpoints:
  GET /api/token/?identity=<identity>   -> returns a JWT access token
  GET/POST /api/voice/                   -> returns TwiML for an incoming/outgoing call

Frontend (React)
----------------
- From frontend directory: npm install
- Start dev server (it proxies to Django):
    npm start

The React app will fetch a token from /api/token/?identity=<name> and initialize the Twilio Device.

Notes
-----
- This is a working starting point. You should secure endpoints, add authentication,
  and adapt to production deployment needs.
