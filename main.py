import os
import csv
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

STRIPE_DONATION_LINK = "https://donate.stripe.com/YOUR_STRIPE_LINK_HERE"

def get_gmail_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "Error: 'credentials.json' not found. "
                    "Please download OAuth client secrets from Google Cloud Console "
                    "and place the file in this directory."
                )
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def send_email(service, recipient_email, recipient_name, html_template):
    # Personalize template
    html_body = html_template.replace("{{name}}", recipient_name)
    html_body = html_body.replace("{{stripe_link}}", STRIPE_DONATION_LINK)
    
    message = MIMEMultipart('alternative')
    message['to'] = recipient_email
    message['subject'] = "Your Support Makes a Difference - SocialSolidarity Foundation"
    
    # Text fallback
    text_fallback = (
        f"Dear {recipient_name},\n\n"
        "Thank you for connecting with us. Your support makes an immediate difference "
        "in our local upskilling and workforce vocational development program.\n\n"
        f"Support with a donation here: {STRIPE_DONATION_LINK}\n\n"
        "With gratitude,\n"
        "The SocialSolidarity Foundation Team"
    )
    
    message.attach(MIMEText(text_fallback, 'plain'))
    message.attach(MIMEText(html_body, 'html'))
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    
    try:
        service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        print(f"✅ Email successfully sent to {recipient_name} ({recipient_email})")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {repr(e)}")

def main():
    if not os.path.exists('template.html'):
        print("❌ Error: template.html not found.")
        return
        
    if not os.path.exists('contacts.csv'):
        print("❌ Error: contacts.csv not found.")
        return

    with open('template.html', 'r', encoding='utf-8') as f:
        html_template = f.read()

    print("🔐 Initializing Gmail API connection...")
    try:
        service = get_gmail_service()
    except Exception as e:
        print(f"❌ Authentication failed: {repr(e)}")
        return

    print("📬 Batch processing contacts.csv...")
    with open('contacts.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get('name', '').strip()
            email = row.get('email', '').strip()
            
            if name and email:
                send_email(service, email, name, html_template)
            else:
                print(f"⚠️ Skipping invalid row: {row}")

if __name__ == '__main__':
    main()
