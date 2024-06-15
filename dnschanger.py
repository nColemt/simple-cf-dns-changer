import requests
import schedule
import time


api_token = " "
zone_id = " "

# API endpoint
base_url = "https://api.cloudflare.com/client/v4"

# Headers
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# DNS record details
record_name = " " # Specified DNS record name
new_ip = " " # replace the new given ip

def list_dns_records():
    url = f"{base_url}/zones/{zone_id}/dns_records"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching DNS records:", response.status_code, response.text)
        return {"success": False, "errors": response.json()}

def update_dns_record(record_id, new_type, content):
    url = f"{base_url}/zones/{zone_id}/dns_records/{record_id}"
    data = {
        "type": new_type,
        "name": record_name,
        "content": content,
        "ttl": 1,  # Auto
        "proxied": False
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error updating DNS record:", response.status_code, response.text)
        return {"success": False, "errors": response.json()}

def change_record_to_a():
    # List all DNS records
    records = list_dns_records()

    if records['success']:
        found = False
        for record in records['result']:
            print(f"Found record: {record['name']} - Type: {record['type']} - Content: {record['content']}")
            if record['name'] == record_name and record['type'] == "CNAME":
                record_id = record['id']
                print(f"Changing CNAME record {record_name} to A record with IP {new_ip}")
                response = update_dns_record(record_id, "A", new_ip)
                print(response)
                found = True
                break
        if not found:
            print(f"No CNAME record found with name {record_name}")
    else:
        print("Failed to retrieve DNS records:", records['errors'])

def schedule_task():
    
    scheduled_time = "13:00" # HH:MM
    schedule.every().day.at(scheduled_time).do(change_record_to_a)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule_task()
