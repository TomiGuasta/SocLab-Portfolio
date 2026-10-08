#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splunk to Telegram Alert Dispatcher Script
Portfolio Home Lab - Blue Team Operations
"""

import sys
import os
import json
import urllib.request
import urllib.parse

# Configuration: Can be overridden by environment variables or edited here
BOT_TOKEN = "8683979969:AAHdlRGfEj1bbosPTn2sqdPDtqHGEEyLGic"
CHAT_ID = "8510239173"

def send_telegram_message(message):
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("Error: Telegram Bot Token or Chat ID not configured.", file=sys.stderr)
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("ok", False)
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}", file=sys.stderr)
        return False

def main():
    # Splunk passes arguments to custom alert scripts:
    # arg[1]: results file path (CSV)
    # arg[2]: number of results / count
    # arg[3]: search results trigger reason
    # arg[4]: search name
    # arg[5]: description
    # arg[6]: owner
    # arg[7]: app
    
    if len(sys.argv) < 5:
        print("Usage: telegram_alert.py <results_file> <count> <trigger_reason> <search_name> <description>", file=sys.stderr)
        # Fallback test message if run directly
        if len(sys.argv) == 2 and sys.argv[1] == "--test":
            success = send_telegram_message("🚨 *Test Security Alert*\nSplunk Telegram integration test successful!")
            print("Test message sent successfully!" if success else "Test message failed.")
            sys.exit(0 if success else 1)
        sys.exit(1)
        
    results_file = sys.argv[1]
    count = sys.argv[2]
    reason = sys.argv[3]
    search_name = sys.argv[4]
    description = sys.argv[5] if len(sys.argv) > 5 else "No description provided."
    
    # Severity mapping based on search name
    if "sql" in search_name or "auditd" in search_name:
        severity_emoji = "🚨🔥 [CRITICAL/HIGH]"
    elif "brute" in search_name or "xss" in search_name:
        severity_emoji = "⚠️ [MEDIUM]"
    else:
        severity_emoji = "ℹ️ [LOW]"

    message = (
        f"{severity_emoji} *SECURITY ALERT: {search_name}*\n\n"
        f"📝 *Description:* {description}\n"
        f"🔢 *Events Count:* {count}\n"
        f"🔍 *Trigger Reason:* {reason}\n"
        f"📂 *Results File:* `{os.path.basename(results_file)}`\n\n"
        f"_Home Lab SIEM - Splunk Detection Engine_"
    )
    
    success = send_telegram_message(message)
    if success:
        print("Telegram alert sent successfully.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
