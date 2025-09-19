README
Twilio Voice Agent – Django + React

This project demonstrates how to build a full-stack voice calling app using Django (backend) and React (frontend) with Twilio Programmable Voice.

🔹 Features:

🎤 Make and receive calls through Twilio Voice SDK

🧑‍💼 Default sales agent identity (sales_agent) for handling incoming calls

🌍 Call either another client identity or an external phone number

🔐 Secure token generation with Django backend

⚡ React frontend with a simple UI to call, accept, and hang up

🚀 Quick Start

Clone & install backend

cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Configure Twilio

Copy .env.example → .env

Fill in:

TWILIO_ACCOUNT_SID=ACxxxx
TWILIO_API_KEY_SID=SKxxxx
TWILIO_API_KEY_SECRET=xxxx
TWILIO_PHONE_NUMBER=+1234567890
TWIML_APP_SID=APxxxx


Run frontend

cd frontend
npm install
npm start


Open http://localhost:3000
 and make a test call 🎉
