# Cloudflare DNS Updater

### What len use it has?
* Update your DNS record on Cloudflare just like [No-ip DUC(Dynamic Update Client)](https://www.noip.com/download?page=win) does.
* Some ISP may provide dynamic IP, which may vary when modem is switched on and off. Running the scirpt at a certain time interval may help you maintain the correct DNS record.
* The script uses the public ip of the computer get on [ipify](https://api.ipify.org/) to update the ip address.

### Usage
1. Configure your data in config.py
    * ZONE_ID: You can find your zone id on Overview tab in Cloudflare.
    * X_AUTH_KEY: You can find the authkey in My Settings -> API Key -> Global API Key
    * X_AUTH_EMAIL: Your Cloudflare login email
    * wanted_type: Condition of filtering, leaving wanted DNS record type only.
    * wanted_name: Same as above, but "name" column this time.
2. Run cloudflare_dns_update.py, the script will process shits for you.
3. Run cloudflare_dns_update.py at any time you want, or running main() from cloudflare_dns_update.py
