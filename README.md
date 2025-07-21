# WhatsApp Bulk Sender
An automated tool to send personalized WhatsApp messages in bulk using a simple web UI. It supports file uploads (CSV, Excel, TXT) and works through WhatsApp Web with your existing account.

🔧 Features
📄 Upload contact files (.csv, .xlsx, .xls, .txt)

💬 Type and send a message to all contacts

🌐 Uses Selenium to open WhatsApp Web and send messages

📊 Displays success/failure status in the UI

🔁 Persists user session using Chrome profile for faster future logins

🛡️ CORS enabled for cross-origin frontend access

🗂️ Project Structure
graphql
Copy
Edit
.
├── backend/
│   ├── automator.py          # Main FastAPI server + WhatsApp logic
│   └── uploads/              # Uploaded contact files
├── frontend/
│   ├── FileUpload.jsx        # File upload input component
│   ├── MessageInput.jsx      # Message input form
│   ├── StatusDisplay.jsx     # Shows status messages
│   └── App.js                # Main React component
├── numbers.txt               # Generated: contains extracted phone numbers
├── message.txt               # Generated: contains user message
└── README.md
🚀 Getting Started
Backend (FastAPI + Selenium)
🔧 Prerequisites
Python 3.9+

Google Chrome (latest)

ChromeDriver (auto-managed via webdriver_manager)

📦 Installation
bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt is not available, manually install:

bash
Copy
Edit
pip install fastapi uvicorn pandas openpyxl python-multipart selenium webdriver-manager
▶️ Run the backend
bash
Copy
Edit
python automator.py
It will start the API server at: http://localhost:8000

Frontend (React)
⚙️ Setup
bash
Copy
Edit
cd frontend
npm install
▶️ Start
bash
Copy
Edit
npm start
📋 Usage Instructions
Open the React frontend in browser (http://localhost:3000)

Upload a .csv, .xlsx, .xls, or .txt file containing phone numbers

Type the message you want to send

Click Send

WhatsApp Web will open in a Chrome window:

If not already logged in, scan the QR code

Messages will be sent one by one with a delay (configurable)

📁 File Format
✅ Supported file types:
.csv

.xlsx / .xls

.txt

📌 Expected column names:
phone, mobile, number, contact (case-insensitive)

If no match, it will use the first column

✅ Example (CSV):
cs
Copy
Edit
phone,name
919999999999,John
918888888888,Alice
⚙️ Configuration
Inside automator.py:

DELAY_BETWEEN_CONTACTS: delay between sending messages

USER_DATA_DIR: to persist Chrome session (no repeated QR scans)

✅ Status Handling
StatusDisplay.jsx shows:

✅ Success: Messages sent successfully

❌ Error: File issues or failed messages

📊 Contacts processed

🧪 API Endpoints
POST /send-message
Parameter	Type	Description
message	string (form)	Message to send
file	UploadFile	Contact list file

Returns:

json
Copy
Edit
{
  "status": "success",
  "message": "Messages sent successfully to 100 contacts!",
  "contacts_processed": 100
}
🔐 Notes
The script opens a real Chrome browser using your current user profile

Never use this tool for spam or unsolicited messaging. WhatsApp may restrict or block your account

🧑‍💻 Author
Avanindra Vijay
💼 AI Developer | Intern @ BISAG-N
🌐 linkedin.com/in/avanindra
🐱 github.com/avanindra

