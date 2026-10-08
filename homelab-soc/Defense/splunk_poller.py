#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Splunk Free REST API Alert Poller & Telegram Dispatcher
Portfolio Home Lab - Blue Team Operations
Bypasses Splunk Free edition alerting limitations by querying the REST API periodically.
"""

import sys
import os
import json
import ssl
import urllib.request
import urllib.parse
import base64
import time

# Import Virtual Firewall Manager
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "04_Tooling"))
try:
    from firewall_manager import VirtualFirewall
    FW = VirtualFirewall()
except ImportError:
    FW = None
    print("[!] Warning: firewall_manager.py not found. Automatic blocking disabled.")

# Configuration via Environment Variables or defaults
SPLUNK_URL = os.environ.get("SPLUNK_URL", "https://localhost:8089")
SPLUNK_USER = os.environ.get("SPLUNK_USER", "admin")
SPLUNK_PASSWORD = os.environ.get("SPLUNK_PASSWORD", "tomi1234")

BOT_TOKEN = "8683979969:AAHdlRGfEj1bbosPTn2sqdPDtqHGEEyLGic"
CHAT_ID = "8510239173"

# Security Detection Queries (Matching savedsearches.conf)
DETECTION_QUERIES = [
    {
        "name": "ssh_brute_force_detection",
        "description": "Multiple failed SSH login attempts detected from a single source IP.",
        "search": 'search index=main (sourcetype=linux_secure OR sourcetype=auth) "Failed password" | stats count by src_ip, user | where count >= 5',
        "severity": "⚠️ [MEDIUM]"
    },
    {
        "name": "dvwa_brute_force_detection",
        "description": "Multiple HTTP 401 unauthorized login attempts against DVWA web application.",
        "search": 'search index=main sourcetype=access_combined status=401 | stats count by clientip, uri | where count > 10',
        "severity": "⚠️ [MEDIUM]"
    },
    {
        "name": "gobuster_fuzzing_detection",
        "description": "High volume of 404/403 HTTP status responses indicating directory fuzzing/enumeration.",
        "search": 'search index=main sourcetype=access_combined (status=404 OR status=403) | stats count by clientip | where count > 50',
        "severity": "⚠️ [MEDIUM]"
    },
    {
        "name": "sql_injection_detection",
        "description": "Potential SQL Injection payload patterns detected in HTTP request URIs.",
        "search": 'search index=main sourcetype=access_combined (uri="*UNION*SELECT*" OR uri="*OR*=*\'") | stats count by clientip, uri',
        "severity": "🚨🔥 [CRITICAL/HIGH]"
    },
    {
        "name": "xss_attack_detection",
        "description": "Cross-Site Scripting (XSS) script tag injection detected in HTTP URIs.",
        "search": 'search index=main sourcetype=access_combined (uri="*%3Cscript%3E*") | stats count by clientip, uri',
        "severity": "⚠️ [MEDIUM]"
    },
    {
        "name": "auditd_sensitive_file_modification",
        "description": "Critical system file modification detected by auditd (/etc/passwd, shadow, sudoers).",
        "search": 'search index=main (key=passwd_changes OR key=shadow_changes OR key=sudoers_changes) | table _time, host, exe, uid, success, key',
        "severity": "🚨🔥 [CRITICAL/HIGH]"
    }
]

def send_telegram_message(message):
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("[!] Error: Telegram Bot Token or Chat ID not configured.", file=sys.stderr)
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("ok", False)
    except Exception as e:
        print(f"[!] Failed to send Telegram alert: {e}", file=sys.stderr)
        return False

def run_splunk_oneshot_search(search_query):
    url = f"{SPLUNK_URL}/services/search/jobs/oneshot"
    
    # Splunk REST API expects form-urlencoded data
    data = urllib.parse.urlencode({
        "search": search_query,
        "output_mode": "json",
        "earliest_time": "-10m", # Look back 10 minutes
        "latest_time": "now"
    }).encode("utf-8")
    
    # Basic Auth header
    auth_str = f"{SPLUNK_USER}:{SPLUNK_PASSWORD}"
    auth_encoded = base64.b64encode(auth_str.encode("ascii")).decode("ascii")
    
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    # Bypass self-signed SSL certificates commonly used in lab Splunk instances
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            result_data = response.read().decode("utf-8")
            return json.loads(result_data)
    except Exception as e:
        print(f"[!] Splunk REST API error for query '{search_query[:30]}...': {e}", file=sys.stderr)
        return None

def main():
    print(f"[*] Starting Splunk Poller check at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if SPLUNK_PASSWORD == "changeme":
        print("[!] Warning: Using default SPLUNK_PASSWORD 'changeme'. Set SPLUNK_PASSWORD env var if needed.", file=sys.stderr)
        
    alerts_triggered = 0
    
    for detection in DETECTION_QUERIES:
        name = detection["name"]
        desc = detection["description"]
        query = detection["search"]
        severity = detection["severity"]
        
        print(f"[*] Checking detection: {name}...")
        result = run_splunk_oneshot_search(query)
        
        if result and "results" in result:
            results = result["results"]
            count = len(results)
            
            if count > 0:
                print(f"[!] ALERT TRIGGERED: {name} ({count} events found)")
                alerts_triggered += 1
                
                # Extract attacker IPs
                attacker_ips = []
                if FW:
                    for res in results:
                        ip = res.get("src_ip") or res.get("clientip")
                        if ip and ip != "unknown":
                            attacker_ips.append(ip)
                
                ip_display = ", ".join(set(attacker_ips)) if attacker_ips else "N/A"

                # Format message
                message = (
                    f"{severity} *SECURITY ALERT: {name}*\n\n"
                    f"📝 *Description:* {desc}\n"
                    f"🎯 *Attacker IP(s):* `{ip_display}`\n"
                    f"🔢 *Events Count:* {count}\n"
                    f"🕒 *Timestamp:* `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
                    f"_Home Lab SIEM - Splunk Free REST API Poller_"
                )
                
                send_telegram_message(message)

                # Automatic Mitigation (Firewall)
                if FW and attacker_ips:
                    for ip in set(attacker_ips):
                        blocked = FW.add_block_rule(ip, f"Automated block: {name}")
                        if blocked:
                            fw_message = (
                                f"🛡️ *FIREWALL ACTIVE RESPONSE (SOAR)*\n\n"
                                f"🚫 *Blocked IP:* `{ip}`\n"
                                f"📝 *Reason:* Automated block: {name}\n"
                                f"🕒 *Timestamp:* `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n\n"
                                f"_Home Lab Virtual Firewall (FW-01)_"
                            )
                            send_telegram_message(fw_message)
            else:
                print(f"    [-] No matches for {name}.")
        else:
            print(f"    [-] Could not retrieve results for {name}.")
            
    print(f"[*] Polling complete. Total alerts triggered: {alerts_triggered}")

if __name__ == "__main__":
    main()
