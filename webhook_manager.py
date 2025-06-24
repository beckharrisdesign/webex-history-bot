#!/usr/bin/env python3
"""
Webex Webhook Management Script
Helps manage webhooks for your Webex bot via the API
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_ACCESS_TOKEN = os.getenv('BOT_ACCESS_TOKEN', '')
WEBEX_WEBHOOKS_URL = 'https://webexapis.com/v1/webhooks'

def get_headers():
    """Get the authorization headers for API calls"""
    return {
        'Authorization': f'Bearer {BOT_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

def list_webhooks():
    """List all existing webhooks for the bot"""
    print("🔍 Fetching existing webhooks...")
    
    response = requests.get(WEBEX_WEBHOOKS_URL, headers=get_headers())
    
    if response.status_code == 200:
        webhooks = response.json().get('items', [])
        print(f"✅ Found {len(webhooks)} webhook(s):")
        
        for i, webhook in enumerate(webhooks, 1):
            print(f"\n{i}. Webhook ID: {webhook['id']}")
            print(f"   Name: {webhook.get('name', 'N/A')}")
            print(f"   Target URL: {webhook.get('targetUrl', 'N/A')}")
            print(f"   Resource: {webhook.get('resource', 'N/A')}")
            print(f"   Event: {webhook.get('event', 'N/A')}")
            print(f"   Status: {webhook.get('status', 'N/A')}")
        
        return webhooks
    else:
        print(f"❌ Error fetching webhooks: {response.status_code}")
        print(f"Response: {response.text}")
        return []

def create_webhook(target_url, name="Webex History Bot Webhook"):
    """Create a new webhook"""
    print(f"🚀 Creating new webhook for {target_url}...")
    
    webhook_data = {
        "name": name,
        "targetUrl": target_url,
        "resource": "messages",
        "event": "created"
    }
    
    response = requests.post(WEBEX_WEBHOOKS_URL, headers=get_headers(), json=webhook_data)
    
    if response.status_code == 200:
        webhook = response.json()
        print("✅ Webhook created successfully!")
        print(f"   Webhook ID: {webhook['id']}")
        print(f"   Target URL: {webhook['targetUrl']}")
        return webhook
    else:
        print(f"❌ Error creating webhook: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def update_webhook(webhook_id, new_target_url, name="Webex History Bot Webhook"):
    """Update an existing webhook"""
    print(f"🔄 Updating webhook {webhook_id} to {new_target_url}...")
    
    webhook_data = {
        "name": name,
        "targetUrl": new_target_url
    }
    
    response = requests.put(f"{WEBEX_WEBHOOKS_URL}/{webhook_id}", headers=get_headers(), json=webhook_data)
    
    if response.status_code == 200:
        webhook = response.json()
        print("✅ Webhook updated successfully!")
        print(f"   Webhook ID: {webhook['id']}")
        print(f"   New Target URL: {webhook['targetUrl']}")
        return webhook
    else:
        print(f"❌ Error updating webhook: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def delete_webhook(webhook_id):
    """Delete a webhook"""
    print(f"🗑️ Deleting webhook {webhook_id}...")
    
    response = requests.delete(f"{WEBEX_WEBHOOKS_URL}/{webhook_id}", headers=get_headers())
    
    if response.status_code == 204:
        print("✅ Webhook deleted successfully!")
        return True
    else:
        print(f"❌ Error deleting webhook: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    """Main interactive menu"""
    if not BOT_ACCESS_TOKEN:
        print("❌ Error: BOT_ACCESS_TOKEN not found in environment variables!")
        print("Please check your .env file and make sure BOT_ACCESS_TOKEN is set.")
        return
    
    print("🤖 Webex Bot Webhook Manager")
    print("=" * 40)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. List existing webhooks")
        print("2. Create new webhook")
        print("3. Update existing webhook")
        print("4. Delete webhook")
        print("5. Quick update to port 3000 (localhost)")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            list_webhooks()
            
        elif choice == '2':
            target_url = input("Enter the target URL (e.g., https://your-tunnel.trycloudflare.com/webhook): ").strip()
            if target_url:
                create_webhook(target_url)
            else:
                print("❌ Invalid URL provided")
                
        elif choice == '3':
            webhooks = list_webhooks()
            if webhooks:
                webhook_id = input("Enter the webhook ID to update: ").strip()
                new_url = input("Enter the new target URL: ").strip()
                if webhook_id and new_url:
                    update_webhook(webhook_id, new_url)
                else:
                    print("❌ Invalid webhook ID or URL provided")
            
        elif choice == '4':
            webhooks = list_webhooks()
            if webhooks:
                webhook_id = input("Enter the webhook ID to delete: ").strip()
                if webhook_id:
                    confirm = input(f"Are you sure you want to delete webhook {webhook_id}? (y/N): ").strip().lower()
                    if confirm == 'y':
                        delete_webhook(webhook_id)
                    else:
                        print("❌ Delete cancelled")
                else:
                    print("❌ Invalid webhook ID provided")
            
        elif choice == '5':
            print("🚀 Quick update for local development on port 3000")
            tunnel_url = input("Enter your tunnel URL (e.g., https://abc-def-123.trycloudflare.com): ").strip()
            if tunnel_url:
                # Remove trailing slash and add /webhook
                tunnel_url = tunnel_url.rstrip('/')
                webhook_url = f"{tunnel_url}/webhook"
                
                # Get existing webhooks
                webhooks = list_webhooks()
                
                if webhooks:
                    # Update the first webhook (assuming you only have one)
                    webhook_id = webhooks[0]['id']
                    update_webhook(webhook_id, webhook_url)
                else:
                    # Create new webhook
                    create_webhook(webhook_url)
            else:
                print("❌ Invalid tunnel URL provided")
                
        elif choice == '6':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
