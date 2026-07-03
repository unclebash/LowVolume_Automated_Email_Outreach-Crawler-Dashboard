import os
import csv

def show_dashboard():
    contacts_file = 'contacts.csv'
    template_file = 'template.html'
    
    print("=" * 60)
    print("📢 EMAIL OUTREACH & CRAWLER STATUS DASHBOARD")
    print("=" * 60)
    
    # 1. Check template
    if os.path.exists(template_file):
        print(f"✅ Email template loaded: {template_file}")
    else:
        print(f"❌ Email template missing: {template_file}")
        
    # 2. Check contacts list
    if os.path.exists(contacts_file):
        try:
            with open(contacts_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                print(f"📋 Total contacts in list: {len(rows)}")
                
                # Show first 5 contacts
                print("\n   Recent Contacts:")
                for i, row in enumerate(rows[:5]):
                    name = row.get('name', 'N/A')
                    email = row.get('email', 'N/A')
                    print(f"    - {name} ({email})")
                if len(rows) > 5:
                    print(f"    ... and {len(rows) - 5} more.")
        except Exception as e:
            print(f"❌ Error reading {contacts_file}: {repr(e)}")
    else:
        print(f"❌ Contacts file missing: {contacts_file}")
        
    # 3. Check sheet tokens
    if os.path.exists('sheets_token.json'):
        print("✅ Google Sheets integration token is active.")
    else:
        print("ℹ️ Google Sheets token not initialized (run sheets_client.py to link).")
        
    print("=" * 60)

if __name__ == '__main__':
    show_dashboard()
