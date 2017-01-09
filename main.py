import requests
import json
import datetime
from config import *

HEADERS         = { "Content-Type"  : "application/json",
                    "X-Auth-Key"    : X_AUTH_KEY,
                    "X-Auth-Email"  : X_AUTH_EMAIL
                }
URL_DNS_RECORDS             = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{dns_id}"
URL_ZONE                    = "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"

def get_ip_address():
    ip = requests.get('https://api.ipify.org').text
    return ip

def update_dns(dns_record):
    url     = URL_DNS_RECORDS.format(zone_id= ZONE_ID, dns_id= dns_record["id"])
    payload = { "type"      : dns_record["type"],
                "name"      : dns_record["name"],
                "content"   : dns_record["content"],
                "proxied"   : dns_record["proxied"],
                }
    req     = requests.put(url, headers=HEADERS, data=json.dumps(payload))
    info = "|%5s|%15s|%15s|%5s|" % (dns_record["type"], dns_record["name"], dns_record["content"], dns_record["proxied"])
    if req.status_code == 200:
        log("[%s][O][200] Successfully updated DNS record of %s" % (time_stamp(), info))
    else:
        log("[%s][*][%i] Failed to update DNS record of %s" % (time_stamp(), req.status_code, info))

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
    if not dns_list_dict:
        return
    for dns in dns_list_dict:
        if dns['type'] in wanted_type and dns['name'] in wanted_name:
            wanted_list.append(dns)
    log("[%s][-][---] %i filtrated DNS record(s)" % (time_stamp(), len(wanted_list)))
    return wanted_list

def time_stamp():
    return '{:%Y-%m-%d|%H:%M:%S}'.format(datetime.datetime.now())

def log(s):
    print(s)

if __name__ == "__main__":
    dns_list_dict = get_dns_list_dict()
    dns_update_data = get_wanted_dns_list(dns_list_dict)
    if dns_update_data:
        for i in dns_update_data:
            i['data'] = get_ip_address()
        for dns_record in dns_update_data:
            update_dns(dns_record)

