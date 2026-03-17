# Import module to execute system commands (like 'arp -a')
import subprocess

# Import time module to add delay between scans
import time

# Import regular expressions module to extract IP and MAC addresses from text
import re

# For API calls
import requests 

# Backend API URL (Node.js server pe hum is route ko banayenge)
BACKEND_URL = "http://localhost:3000/api/alerts"


# Dictionary to store trusted IP → MAC mappings
# Example:
# {
#   "192.168.1.1": "c0-25-2f-d5-62-0e",
#   "192.168.1.118": "08-00-27-63-b0-05"
# }
trusted_table = {}


# Function to retrieve the ARP table from the operating system
def get_arp_table():
    
    # Run the Windows command "arp -a" to get ARP cache
    # subprocess.check_output executes the command and returns the output
    output = subprocess.check_output("arp -a").decode()

    # Convert the output from bytes to a readable string
    return output


# Main IDS monitoring function
def monitor():

    # Infinite loop so IDS keeps monitoring continuously
    while True:

        # Get current ARP table
        arp_output = get_arp_table()

        # Split output into individual lines
        lines = arp_output.split("\n")

        # Process each line one by one
        for line in lines:

            # Use regex to match valid IP and MAC address entries
            # Example line matched:
            # 192.168.1.1    c0-25-2f-d5-62-0e
            match = re.match(r"\s*(\d+\.\d+\.\d+\.\d+)\s+([a-f0-9\-]+)", line.lower())

            # If the line contains a valid IP-MAC mapping
            if match:

                # Extract IP address from the line
                ip = match.group(1)

                # Extract MAC address from the line
                mac = match.group(2)

                # Ignore broadcast MAC addresses
                # Broadcast entries are not useful for spoofing detection
                if mac == "ff-ff-ff-ff-ff-ff":
                    continue

                # Check if the IP already exists in our trusted table
                if ip in trusted_table:

                    # Compare stored MAC with current MAC
                    # If different → possible ARP spoofing attack
                    if trusted_table[ip] != mac:

                        print("\n ARP SPOOFING DETECTED")
                        print("IP:", ip)
                        print("Original MAC:", trusted_table[ip])
                        print("Fake MAC:", mac)

                        # --- NAYA CODE: Backend ko Data Bhejna ---
                        alert_data = {
                            "attacker_mac": mac,
                            "target_ip": ip
                        }
                        
                        try:
                            # Send data to Node.js server as JSON
                            response = requests.post(BACKEND_URL, json=alert_data)
                            print(f"Alert sent to Database! Server Status: {response.status_code}")
                        except Exception as e:
                            print("Backend server se connect nahi ho paaya. Kya server chal raha hai?")
                        # ------------------------------------------

                else:
                    # If IP not seen before, add it to trusted table
                    trusted_table[ip] = mac

                    # Print mapping for new devices discovered on the network
                    print(f"Mapped: {ip} -> {mac}")

        # Wait 3 seconds before scanning ARP table again
        time.sleep(3)


# Start the IDS monitoring system
monitor()