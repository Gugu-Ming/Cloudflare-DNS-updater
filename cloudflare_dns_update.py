import requests
import json
import datetime
import time # Used to set the delay between checks & updates
import logging
from config import *

HEADERS         = { "Content-Type"  : "application/json",
                    "X-Auth-Key"    : X_AUTH_KEY,
                    "X-Auth-Email"  : X_AUTH_EMAIL }
URL_DNS_RECORDS = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_id}"
URL_ZONE        = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

logging.basicConfig(filename='updates.log', level=logging.INFO)

def main():
    while True: # Run This Indefinetly 
        ip = get_ip_address()
        if ip:
            dns_list_dict = get_dns_list_dict()
            if dns_list_dict:
                dns_update_data = get_wanted_dns_list(dns_list_dict)
                for dns_record in dns_update_data:
                    update_dns(dns_record, ip)
        time.sleep(delay) 

def get_ip_address():
    try:
        ip = requests.get('https://api.ipify.org').text
        return ip
    except requests.exceptions.ConnectionError:
        log("[%s][*][---] Failed to get ip from ipify" % time_stamp(), 'error')
        return False

def update_dns(dns_record, ip):
    url     = URL_DNS_RECORDS.format(zone_id= ZONE_ID, dns_id= dns_record["id"])
    payload = { "type"      : dns_record["type"],
                "name"      : dns_record["name"],
                "content"   : ip,
                "proxied"   : dns_record["proxied"], }
    req     = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    if req.status_code == 200:
        new_dns_record = json.loads(req.text)["result"]
        new_info = "|%5s|%15s|%15s|%5s|" % (new_dns_record["type"], new_dns_record["name"], new_dns_record["content"], new_dns_record["proxied"])
        log("[%s][O][200] Successfully updated DNS record, now is: %s" % (time_stamp(), new_info))
    else:
        original_info = "|%5s|%15s|%15s|%5s|" % (dns_record["type"], dns_record["name"], dns_record["content"], dns_record["proxied"])
        log("[%s][*][%i] Failed to update DNS record of %s" % (time_stamp(), req.status_code, original_info))

def get_dns_list_dict():
    url = URL_ZONE.format(zone_id=ZONE_ID)
    req = requests.get(url, headers=HEADERS)
    result = json.loads(req.text)["result"]
    if req.status_code == 200:
        log("[%s][O][200] Successfully get DNS record(s) list of length %i" % (time_stamp(), len(result)))
    else:
        log("[%s][*][%i] Failed to get DNS record(s) list" % (time_stamp(), req.status_code))
    return result

def get_wanted_dns_list(dns_list_dict):
    wanted_list = []
    for dns in dns_list_dict:
        if dns['type'] in wanted_type and dns['name'] in wanted_name:
            wanted_list.append(dns)
    log("[%s][-][---] %i filtrated DNS record(s)" % (time_stamp(), len(wanted_list)))
    return wanted_list

def time_stamp():
    return '{:%Y-%m-%d|%H:%M:%S}'.format(datetime.datetime.now())

def log(s, level='info'):
    if level == 'info':
        logging.info(s)
    elif level == 'error':
        logging.error(s)
    print(s)

if __name__ == "__main__":
    main()

