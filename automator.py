from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import subprocess
import os
import time
import pandas as pd
import uvicorn

# ======================= STYLING FOR TERMINAL =======================
class Style:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'
    RESET = '\033[0m'

# ======================= CONFIGURATION =======================
DELAY_BETWEEN_CONTACTS = 10  # seconds (reduced for better performance)
WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'
USER_DATA_DIR = os.path.join(os.getcwd(), "chrome_user_data")

def send_whatsapp_messages():
    """Function to handle WhatsApp message sending"""
    
    # ======================= CHROME OPTIONS =======================
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    # Keep browser open for debugging (comment out in production)
    # chrome_options.add_experimental_option("detach", True)

    # ======================= LOAD MESSAGE =======================
    try:
        with open("message.txt", "r", encoding="utf8") as f:
            raw_message = f.read().strip()
            print(Style.YELLOW + "\nThis is your message:")
            print(Style.GREEN + raw_message + "\n" + Style.RESET)
            message = quote(raw_message)
    except FileNotFoundError:
        print(Style.RED + "❌ 'message.txt' not found." + Style.RESET)
        return False

    # ======================= LOAD NUMBERS =======================
    try:
        with open("numbers.txt", "r") as f:
            numbers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(Style.RED + "❌ 'numbers.txt' not found." + Style.RESET)
        return False

    print(Style.RED + f"\nWe found {len(numbers)} numbers in the file.\n" + Style.RESET)

    # ======================= SETUP CHROME DRIVER =======================
    print("Launching Chrome browser...")
    os.environ["WDM_LOG_LEVEL"] = "0"
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # ======================= LOGIN TO WHATSAPP =======================
        driver.get(WHATSAPP_WEB_URL)
        print(Style.MAGENTA + "Please log in to WhatsApp Web and ensure chats are visible..." + Style.RESET)
        
        # Wait for WhatsApp to load - try multiple selectors
        try:
            # First try to wait for the chat list (logged in state)
            WebDriverWait(driver, 30).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='chat-list']")),
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'chat-list')]"))
                )
            )
            print(Style.GREEN + "WhatsApp Web loaded successfully!" + Style.RESET)
        except:
            # If chat list not found, check if we need to scan QR code
            try:
                qr_code = driver.find_element(By.XPATH, "//div[@data-testid='qr-code']")
                if qr_code:
                    print(Style.YELLOW + "QR Code detected. Please scan the QR code to log in..." + Style.RESET)
                    # Wait longer for QR code scan
                    WebDriverWait(driver, 120).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='chat-list']")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']")),
                            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid='chat-list']"))
                        )
                    )
                    print(Style.GREEN + "Successfully logged in!" + Style.RESET)
            except:
                print(Style.YELLOW + "Waiting for WhatsApp Web to load completely..." + Style.RESET)
                # Give more time and try different approach
                time.sleep(10)
                
                # Check if page is loaded by looking for any WhatsApp elements
                try:
                    WebDriverWait(driver, 30).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'app-wrapper')]")),
                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'landing-wrapper')]")),
                            EC.presence_of_element_located((By.XPATH, "//div[@id='app']"))
                        )
                    )
                    print(Style.GREEN + "WhatsApp Web interface loaded!" + Style.RESET)
                except:
                    print(Style.RED + "Failed to load WhatsApp Web. Please check your internet connection." + Style.RESET)
                    return False

        # ======================= SEND MESSAGES =======================
        successful_sends = 0
        failed_sends = 0
        
        for index, number in enumerate(numbers, start=1):
            print(Style.YELLOW + f"{index}/{len(numbers)} => Sending message to {number}" + Style.RESET)
            url = f"https://web.whatsapp.com/send?phone={number}&text={message}"

            try:
                driver.get(url)
                
                # Wait for page to load
                time.sleep(5)
                
                # Check if we need to refresh or if there's an error
                try:
                    # Look for various possible send button selectors
                    send_button = None
                    selectors = [
                        "//button[@data-testid='send']",
                        "//span[@data-testid='send']",
                        "//button[contains(@class, 'send')]",
                        "//span[contains(@aria-label, 'Send')]",
                        "//button[contains(@aria-label, 'Send')]"
                    ]
                    
                    for selector in selectors:
                        try:
                            send_button = WebDriverWait(driver, 15).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            break
                        except:
                            continue
                    
                    if send_button:
                        # Scroll to button and click
                        driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
                        time.sleep(1)
                        send_button.click()
                        time.sleep(2)  # Wait for message to be sent
                        
                        print(Style.GREEN + f"✅ Message sent to {number}" + Style.RESET)
                        successful_sends += 1
                    else:
                        print(Style.RED + f"❌ Send button not found for {number}" + Style.RESET)
                        failed_sends += 1
                        
                except Exception as send_error:
                    print(Style.RED + f"❌ Failed to send message to {number}. Error: {str(send_error)}" + Style.RESET)
                    failed_sends += 1

            except Exception as e:
                print(Style.RED + f"❌ Failed to load chat for {number}. Error: {str(e)}" + Style.RESET)
                failed_sends += 1

            # Wait between messages (except for the last one)
            if index != len(numbers):
                print(Style.MAGENTA + f"⏳ Waiting for {DELAY_BETWEEN_CONTACTS} seconds before next message...\n" + Style.RESET)
                time.sleep(DELAY_BETWEEN_CONTACTS)

        # ======================= RESULTS =======================
        print(Style.GREEN + f"\n📊 RESULTS:" + Style.RESET)
        print(Style.GREEN + f"✅ Successful: {successful_sends}" + Style.RESET)
        print(Style.RED + f"❌ Failed: {failed_sends}" + Style.RESET)
        print(Style.GREEN + f"📱 Total processed: {len(numbers)}" + Style.RESET)

    finally:
        # ======================= CLEANUP =======================
        print(Style.GREEN + "\n🔄 Closing browser..." + Style.RESET)
        driver.quit()
    
    return True

def extract_phone_numbers(file_path):
    """Extract phone numbers from CSV, Excel, or TXT file"""
    try:
        phone_numbers = []
        
        if file_path.endswith('.txt'):
            # Handle TXT files - each line should contain a phone number
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        phone_numbers.append(line)
        
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            phone_numbers = extract_numbers_from_dataframe(df)
        
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            phone_numbers = extract_numbers_from_dataframe(df)
        
        else:
            return []
        
        # Clean phone numbers (remove non-digits and ensure proper format)
        cleaned_numbers = []
        for num in phone_numbers:
            # Remove all non-digit characters
            clean_num = ''.join(filter(str.isdigit, str(num)))
            if clean_num and len(clean_num) >= 10:  # Valid phone number length
                cleaned_numbers.append(clean_num)
        
        return cleaned_numbers
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return []

def extract_numbers_from_dataframe(df):
    """Extract phone numbers from pandas DataFrame"""
    # Look for phone number columns (common names)
    phone_columns = ['phone', 'Phone', 'PHONE', 'mobile', 'Mobile', 'MOBILE', 
                    'number', 'Number', 'NUMBER', 'contact', 'Contact', 'CONTACT']
    
    phone_numbers = []
    for col in phone_columns:
        if col in df.columns:
            phone_numbers = df[col].dropna().astype(str).tolist()
            break
    
    # If no specific column found, use the first column
    if not phone_numbers and len(df.columns) > 0:
        phone_numbers = df.iloc[:, 0].dropna().astype(str).tolist()
    
    return phone_numbers

# ======================= FASTAPI APP =======================
app = FastAPI(title="WhatsApp Bulk Sender API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("uploads", exist_ok=True)

@app.post("/send-message")
async def send_message_endpoint(message: str = Form(...), file: UploadFile = File(...)):
    """API endpoint to receive message and file, then send WhatsApp messages"""
    
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx', '.xls', '.txt')):
            return {"status": "error", "message": "Please upload a valid CSV, Excel, or TXT file."}
        
        # Save uploaded file
        file_path = f"./uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract phone numbers from file
        phone_numbers = extract_phone_numbers(file_path)
        
        if not phone_numbers:
            return {"status": "error", "message": "No valid phone numbers found in the file."}

        # Save message to file
        with open("message.txt", "w", encoding="utf8") as f:
            f.write(message)

        # Save phone numbers to numbers.txt
        with open("numbers.txt", "w") as f:
            for number in phone_numbers:
                f.write(number + "\n")

        print(f"Found {len(phone_numbers)} phone numbers")
        print("Starting WhatsApp message sending...")
        
        # Send messages
        success = send_whatsapp_messages()
        
        if success:
            return {
                "status": "success", 
                "message": f"Messages sent successfully to {len(phone_numbers)} contacts!",
                "contacts_processed": len(phone_numbers)
            }
        else:
            return {"status": "error", "message": "Failed to send messages."}
            
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {str(e)}"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "WhatsApp Bulk Sender API is running!"}

if __name__ == "__main__":
    # If running this file directly, start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)